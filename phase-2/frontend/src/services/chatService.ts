import { ChatApiResponse } from '@/types/chat';

export class ChatAuthError extends Error {
  constructor() {
    super('Authentication expired. Please sign in again.');
    this.name = 'ChatAuthError';
  }
}

export class ChatTimeoutError extends Error {
  constructor() {
    super('The AI agent took too long to respond. Please try again.');
    this.name = 'ChatTimeoutError';
  }
}

export class ChatRateLimitError extends Error {
  constructor(message?: string) {
    super(message ?? 'AI rate limit exceeded. Please try again in a moment.');
    this.name = 'ChatRateLimitError';
  }
}

export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId: string | null,
  token: string
): Promise<ChatApiResponse> {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (response.status === 401) {
    throw new ChatAuthError();
  }

  if (response.status === 429) {
    const data = await response.json().catch(() => ({}));
    throw new ChatRateLimitError(data?.detail ?? undefined);
  }

  if (response.status === 504) {
    throw new ChatTimeoutError();
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    const err = new Error(data?.detail || data?.error || `Request failed with status ${response.status}`);
    (err as any).status = response.status;
    throw err;
  }

  return response.json() as Promise<ChatApiResponse>;
}
