'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { ChatMessage, ChatState, ChatApiMessage } from '@/types/chat';
import { sendChatMessage, ChatAuthError, ChatRateLimitError } from '@/services/chatService';
import { useAuth } from '@/hooks/useAuth';
import { getAccessToken } from '@/hooks/useSession';

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

function conversationKey(userId: string): string {
  return `chat_conversation_id_${userId}`;
}

function mapApiMessage(m: ChatApiMessage): ChatMessage {
  return {
    id: generateId(),
    role: m.role,
    content: m.content,
    toolCalls: m.tool_calls ?? undefined,
    toolOutputs: m.tool_outputs,
    timestamp: m.created_at ?? new Date().toISOString(),
  };
}

export function useChat() {
  const { state: authState } = useAuth();
  const router = useRouter();

  const userId = authState.user?.id ?? '';
  // Get token from session storage instead of auth state
  const getToken = () => getAccessToken() ?? '';

  const getStoredConversationId = (): string | null => {
    if (!userId || typeof window === 'undefined') return null;
    return localStorage.getItem(conversationKey(userId));
  };

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(
    getStoredConversationId
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUserMessage, setLastUserMessage] = useState<string>('');

  const persistConversationId = useCallback(
    (id: string | null) => {
      if (!userId) return;
      if (id) {
        localStorage.setItem(conversationKey(userId), id);
      } else {
        localStorage.removeItem(conversationKey(userId));
      }
      setConversationId(id);
    },
    [userId]
  );

  const applyResponse = useCallback(
    (data: Awaited<ReturnType<typeof sendChatMessage>>) => {
      persistConversationId(data.conversation_id);
      // Replace state with the full canonical history from backend
      setMessages(data.messages.map(mapApiMessage));
      // Notify other parts of the app that todos may have changed
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('todos-updated'));
      }
    },
    [persistConversationId]
  );

  const sendMessage = useCallback(
    async (text: string, overrideConversationId?: string | null) => {
      if (!text.trim() || loading) return;

      setLastUserMessage(text);
      setError(null);
      setLoading(true);

      // Optimistic user message while waiting for backend
      const optimisticId = generateId();
      const optimisticUserMsg: ChatMessage = {
        id: optimisticId,
        role: 'user',
        content: text,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, optimisticUserMsg]);

      const convId =
        overrideConversationId !== undefined
          ? overrideConversationId
          : conversationId;

      try {
        const currentToken = getToken();
        const data = await sendChatMessage(userId, text, convId, currentToken);
        // Full history from backend replaces optimistic message
        applyResponse(data);
      } catch (err: unknown) {
        if (err instanceof ChatAuthError) {
          router.push('/signin');
          return;
        }
        if (err instanceof ChatRateLimitError) {
          setMessages((prev) => prev.filter((m) => m.id !== optimisticId));
          setError(err.message);
          return;
        }
        // 404 = stale conversation_id — retry with null (new conversation)
        if ((err as { status?: number })?.status === 404 && convId !== null) {
          persistConversationId(null);
          setMessages([]);
          setLoading(false);
          await sendMessage(text, null);
          return;
        }
        // Remove optimistic message on error
        setMessages((prev) => prev.filter((m) => m.id !== optimisticId));
        const msg = err instanceof Error ? err.message : 'Something went wrong. Please try again.';
        setError(msg);
      } finally {
        setLoading(false);
      }
    },
    [loading, conversationId, userId, applyResponse, persistConversationId, router, getToken]
  );

  const retry = useCallback(() => {
    if (lastUserMessage) {
      setError(null);
      sendMessage(lastUserMessage);
    }
  }, [lastUserMessage, sendMessage]);

  const state: ChatState = { messages, conversationId, loading, error };

  return { state, sendMessage, retry };
}
