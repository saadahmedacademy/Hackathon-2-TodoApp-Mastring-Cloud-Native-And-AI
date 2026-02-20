// Chat types for 009-chatbot-ui-dashboard

export interface ToolCallSummary {
  toolName: string;
  arguments?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  /** Raw OpenAI-format tool calls on assistant messages */
  toolCalls?: Array<{
    id: string;
    type: string;
    function: { name: string; arguments: string };
  }> | null;
  /** Tool result payload on tool messages */
  toolOutputs?: { tool_call_id: string; name: string; output: Record<string, unknown> };
  timestamp: string;
  isError?: boolean;
}

export interface ChatState {
  messages: ChatMessage[];
  conversationId: string | null;
  loading: boolean;
  error: string | null;
}

export interface ChatRequest {
  message: string;
  conversation_id: string | null;
}

// Matches the backend response shape exactly
export interface ChatApiMessage {
  role: 'user' | 'assistant' | 'tool';
  content: string;
  tool_calls?: Array<{
    id: string;
    type: string;
    function: { name: string; arguments: string };
  }> | null;
  tool_outputs?: { tool_call_id: string; name: string; output: Record<string, unknown> };
  created_at?: string;
}

export interface ChatApiResponse {
  conversation_id: string;
  messages: ChatApiMessage[];
}
