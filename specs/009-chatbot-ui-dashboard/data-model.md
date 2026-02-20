# Data Model: Chatbot UI in Todo Dashboard

**Feature**: 009-chatbot-ui-dashboard
**Date**: 2026-02-16
**Scope**: Frontend-only types (no new DB tables — backend handles persistence)

---

## TypeScript Types

### ChatMessage

```ts
// A single message in the chat UI
export interface ChatMessage {
  id: string;                    // Local UUID (frontend-generated for rendering key)
  role: 'user' | 'assistant';   // Who sent the message
  content: string;              // Message text
  toolCalls?: ToolCallSummary[]; // Present when AI executed tool(s)
  timestamp: string;            // ISO datetime string
  isError?: boolean;            // True when this message represents a failure
}
```

### ToolCallSummary

```ts
// Summary of a single tool execution returned by the backend
export interface ToolCallSummary {
  toolName: string;     // e.g. "add_task", "delete_task"
  input?: string;       // Summarised input (e.g. task description)
  outcome: string;      // e.g. "Task created successfully."
}
```

### ChatState

```ts
// State managed by useChat hook
export interface ChatState {
  messages: ChatMessage[];
  conversationId: string | null;
  loading: boolean;
  error: string | null;
}
```

### ChatRequest (sent to Next.js proxy route)

```ts
export interface ChatRequest {
  message: string;
  conversation_id: string | null;
}
```

### ChatApiResponse (received from Phase-3 backend via proxy)

```ts
export interface ChatApiResponse {
  conversation_id: string;
  messages: Array<{
    role: 'user' | 'assistant';
    content: string;
    tool_calls?: Array<{
      tool_name: string;
      input?: string;
      outcome: string;
    }>;
    created_at?: string;
  }>;
}
```

---

## State Transitions

```
Idle ──[User types]──► HasInput
HasInput ──[Send]──► Loading (disable Send, show spinner)
Loading ──[Success]──► Idle + messages updated + conversationId stored
Loading ──[Error]──► Error state (show Retry) ──[Retry]──► Loading
Loading ──[stale conversationId error]──► Clear localStorage + new conversation ──► Loading
```

---

## localStorage Key Convention

```
Key:   "chat_conversation_id_{user_id}"
Value: UUID string (e.g. "3f2504e0-4f89-11d3-9a0c-0305e82c3301")
```

Cleared when:
- Backend returns 404/invalid conversation error
- User explicitly starts a new conversation (future feature)
