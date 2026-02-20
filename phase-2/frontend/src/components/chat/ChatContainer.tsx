'use client';

import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';
import TypingIndicator from './TypingIndicator';
import ChatInput from './ChatInput';

export default function ChatContainer() {
  const { state, sendMessage, retry } = useChat();
  const { messages, loading, error } = state;

  return (
    <div className="flex flex-col h-full">
      {/* Messages */}
      <MessageList messages={messages} />

      {/* Typing indicator */}
      {loading && <TypingIndicator />}

      {/* Error banner */}
      {error && !loading && (
        <div className="mx-4 mb-2 flex items-center justify-between gap-2 rounded-lg border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive">
          <span>{error}</span>
          <button
            onClick={retry}
            className="shrink-0 rounded px-2 py-1 font-medium hover:bg-destructive/20 transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
