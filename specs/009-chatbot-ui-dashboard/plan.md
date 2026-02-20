# Implementation Plan: Chatbot UI in Todo Dashboard

**Feature**: 009-chatbot-ui-dashboard
**Branch**: 007-refactor-jwt-secret
**Created**: 2026-02-16
**Status**: Ready for Implementation

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase-2 Next.js Frontend                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Dashboard Page  (app/dashboard/page.tsx)                 │   │
│  │                                                            │   │
│  │  ┌──────────────────┐  ┌──────────────────────────────┐  │   │
│  │  │   Task List UI   │  │  ChatDrawerToggle Button      │  │   │
│  │  │  (existing)      │  │  (in Navbar or dashboard)     │  │   │
│  │  └──────────────────┘  └──────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Side Drawer (components/chat/ChatDrawer.tsx)             │   │
│  │                                                            │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  ChatContainer (components/chat/ChatContainer.tsx)  │  │   │
│  │  │   ├── MessageList (MessageList.tsx)                 │  │   │
│  │  │   │    ├── MessageBubble (user / assistant)         │  │   │
│  │  │   │    └── ToolCallCard (collapsible <details>)     │  │   │
│  │  │   ├── TypingIndicator (TypingIndicator.tsx)         │  │   │
│  │  │   └── ChatInput (ChatInput.tsx)                     │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  State: useChat hook (hooks/useChat.ts)                          │
│  API:   chatService (services/chatService.ts)                    │
│  Types: types/chat.ts                                            │
│  Proxy: app/api/chat/route.ts (server-side, hides backend URL)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                    POST /api/chat (browser)
                              │
                    POST /api/chat/route.ts (Next.js proxy)
                              │  reads PHASE3_BACKEND_URL server-side
                              │
                    POST {PHASE3_BACKEND_URL}/api/{user_id}/chat
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    Phase-3 FastAPI Backend                        │
│  chat.py → ConversationService → AIAgentBase → Gemini API       │
│                              → Tool calls → Neon DB              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| Phase-First Correctness | ✅ PASS | Phase-2 frontend remains independently deployable |
| Simplicity Before Scale | ✅ PASS | No streaming, no multi-conversation; minimal new code |
| Clean Evolution | ✅ PASS | Chat added via new components; existing code untouched |
| Deterministic Behavior | ✅ PASS | Frontend is stateless per render; state in hook only |
| Human-Centered UX | ✅ PASS | Drawer, loading states, retry, tool summaries all specified |
| Phase-Specific Standards | ✅ PASS | Phase II tech stack: Next.js, TypeScript, Tailwind CSS |

---

## Phase A – Types & API Contract

**Goal**: Define all TypeScript types and the Next.js proxy route.

### A1 – Create `phase-2/frontend/src/types/chat.ts`

```ts
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCallSummary[];
  timestamp: string;
  isError?: boolean;
}

export interface ToolCallSummary {
  toolName: string;
  input?: string;
  outcome: string;
}

export interface ChatState {
  messages: ChatMessage[];
  conversationId: string | null;
  loading: boolean;
  error: string | null;
}

export interface ChatRequest {
  user_id: string;
  message: string;
  conversation_id: string | null;
}

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

### A2 – Create `phase-2/frontend/src/app/api/chat/route.ts` (Next.js Proxy)

- Read `PHASE3_BACKEND_URL` from `process.env` (server-side only)
- Extract `user_id`, `message`, `conversation_id` from request body
- Forward `Authorization` header from incoming request
- `POST {PHASE3_BACKEND_URL}/api/{user_id}/chat` with `{ message, conversation_id }`
- Return backend JSON as-is; map errors to appropriate HTTP status codes
- Handle 404 from backend (stale conversation_id) → return 404 so frontend can clear localStorage

### A3 – Create `phase-2/frontend/src/services/chatService.ts`

```ts
// Thin wrapper — calls the Next.js proxy route (not the backend directly)
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId: string | null,
  token: string
): Promise<ChatApiResponse>
```

- Calls `POST /api/chat` (the proxy route)
- Attaches `Authorization: Bearer {token}` header
- Throws typed errors for non-2xx responses

---

## Phase B – State Layer (`useChat` Hook)

**Goal**: Create `phase-2/frontend/src/hooks/useChat.ts`

### State managed:
```ts
const [messages, setMessages] = useState<ChatMessage[]>([]);
const [conversationId, setConversationId] = useState<string | null>(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

### Behaviours:

**On mount** (`useEffect`):
- Read `localStorage.getItem('chat_conversation_id_{userId}')` → set `conversationId`
- Restore previous messages from localStorage (serialised JSON) OR just restore `conversationId` and send first follow-up with it (backend returns full history)

**`sendMessage(text: string)`**:
1. Append user message to `messages` (optimistic)
2. Set `loading = true`, `error = null`
3. Call `chatService.sendChatMessage(userId, text, conversationId, token)`
4. On success:
   - Set `conversationId` from response
   - Persist `conversationId` to localStorage
   - Map backend messages → `ChatMessage[]` and update state
5. On 404 (stale conversation):
   - Clear localStorage key
   - Reset `conversationId` to `null`
   - Retry once with `conversation_id: null`
6. On other errors:
   - Set `error` with message
   - Keep `loading = false` (enables Retry)
7. Set `loading = false`

**`retry()`**:
- Re-calls `sendMessage` with the last user message

**Integration with auth**:
- Import `useAuth` to get `state.user.id` and access token from `apiClient`

---

## Phase C – Chat UI Components

**Goal**: Build chat components in `phase-2/frontend/src/components/chat/`

### Component tree:
```
ChatDrawer.tsx          ← drawer shell (overlay + slide animation)
  └── ChatContainer.tsx ← full-height flex layout
        ├── MessageList.tsx  ← scrollable message history
        │     ├── MessageBubble.tsx  ← single message (user/assistant)
        │     └── ToolCallCard.tsx   ← collapsible tool call summary
        ├── TypingIndicator.tsx ← animated dots while loading
        └── ChatInput.tsx ← textarea + send button
```

### `ChatDrawer.tsx`
- Props: `isOpen: boolean`, `onClose: () => void`
- Renders a fixed-position overlay (`z-50`) that slides in from the right
- Width: `w-full sm:w-96` (full on mobile, 384px on ≥sm)
- Close on backdrop click or ✕ button
- Tailwind: `transform transition-transform duration-300 translate-x-full` → `translate-x-0` when open
- Mounts `ChatContainer` inside

### `ChatContainer.tsx`
- Connects to `useChat()` hook
- Renders `MessageList`, `TypingIndicator` (conditional), `ChatInput`
- Full height flex column: messages grow, input fixed at bottom

### `MessageList.tsx`
- `overflow-y-auto` scrollable container
- `useEffect` with `scrollIntoView` on messages change (auto-scroll to bottom)
- Renders `MessageBubble` for each message
- Renders `ToolCallCard` for messages with `toolCalls`

### `MessageBubble.tsx`
- `role === 'user'` → right-aligned, primary color background
- `role === 'assistant'` → left-aligned, secondary/muted background
- `isError` → red tinted background with warning icon
- Timestamp displayed in small text below content

### `ToolCallCard.tsx`
- `<details>` / `<summary>` HTML elements
- Summary line: `🔧 Tool used: {toolName}`
- Expanded: shows `input` (if any) and `outcome`
- Tailwind: bordered, rounded, muted background, `text-sm`

### `TypingIndicator.tsx`
- Three animated dots (CSS `animate-bounce` with staggered delays)
- Only rendered when `loading === true`

### `ChatInput.tsx`
- `<textarea>` (auto-resize, max 3 rows) + Send button
- Send disabled when `value.trim() === ''` or `loading === true`
- Submit on Enter (without Shift); Shift+Enter = newline
- Clears input after successful submit

---

## Phase D – Dashboard Integration

**Goal**: Wire the drawer into the existing dashboard layout.

### Changes to `phase-2/frontend/src/app/dashboard/layout.tsx`

- Add state: `const [chatOpen, setChatOpen] = useState(false)`
- Render `<ChatDrawer isOpen={chatOpen} onClose={() => setChatOpen(false)} />` at the bottom of the layout (outside `<main>`, inside the root div)
- Pass a toggle function or use a context if Navbar needs access

### Changes to `phase-2/frontend/src/components/layout/Navbar.tsx`

- Add a "Chat" button (💬 icon) on the right of the Navbar
- On click: calls the toggle function passed from the layout
- Use `useState` + callback prop pattern (or a lightweight ChatContext if needed)

### No changes to existing task list components, hooks, or API client.

---

## Phase E – UX Enhancements

**Goal**: Polish the experience to meet SC-001–SC-006.

| Enhancement | Implementation |
|-------------|---------------|
| Auto-scroll on new messages | `useEffect(() => ref.scrollIntoView(), [messages])` |
| Retry button | Shown when `error !== null`; calls `retry()` from `useChat` |
| Stale conversation recovery | `useChat` auto-retries with `conversation_id: null` on 404 |
| Send on Enter | `onKeyDown` handler in `ChatInput` |
| Disable Send while loading | `disabled={loading \|\| !value.trim()}` |
| Error clearing on new message | `setError(null)` at start of `sendMessage` |

---

## Phase F – Environment & Deployment

**Goal**: Secure configuration and Vercel deployment readiness.

### `.env.local` additions (not committed):
```
PHASE3_BACKEND_URL=http://localhost:8001
```

### Vercel environment variables:
- Add `PHASE3_BACKEND_URL` as a **server-side** env var in Vercel dashboard (not exposed to client)
- `NEXT_PUBLIC_API_BASE_URL` already exists for Phase-2 backend

### CORS:
- No CORS configuration needed — Next.js proxy route calls Phase-3 server-to-server

### Timeout:
- Set `fetch` timeout of 30 seconds in `chatService.ts` using `AbortController`

---

## File Structure Summary

```
phase-2/frontend/src/
  types/
    chat.ts                          ← NEW: ChatMessage, ToolCallSummary, ChatState, etc.
  services/
    chatService.ts                   ← NEW: sendChatMessage() function
  hooks/
    useChat.ts                       ← NEW: state management hook
  components/
    chat/                            ← NEW directory
      ChatDrawer.tsx
      ChatContainer.tsx
      MessageList.tsx
      MessageBubble.tsx
      ToolCallCard.tsx
      TypingIndicator.tsx
      ChatInput.tsx
  app/
    api/
      chat/
        route.ts                     ← NEW: Next.js proxy route (server-side)
    dashboard/
      layout.tsx                     ← MODIFY: add ChatDrawer + toggle state
  components/
    layout/
      Navbar.tsx                     ← MODIFY: add Chat toggle button
```

**Total new files**: 9
**Modified files**: 2

---

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| Phase-3 backend not accessible from Vercel | Medium | High | Ensure `PHASE3_BACKEND_URL` points to deployed/accessible URL; test proxy route in staging |
| Stale `conversation_id` causes persistent errors | Low | Medium | Auto-recovery logic in `useChat`: on 404, clear localStorage + retry with null |
| Long AI responses cause layout overflow | Low | Low | `overflow-y-auto` on message list; max-height constrains drawer |
| JWT expiry mid-conversation | Low | Medium | 401 response → redirect to signin; existing auth interceptor handles this |
| Drawer obscures content on mobile | Low | Low | Full-width drawer on mobile; backdrop click to close |

---

## Performance Considerations

- Messages stored in React state (not re-fetched from backend on every render)
- `conversation_id` persisted in localStorage (O(1) read on mount)
- No websocket / polling — single fetch per message
- Drawer uses CSS transform (GPU-accelerated) for animation
- `AbortController` prevents zombie requests if user closes drawer mid-flight

---

## Security Checklist

- [x] `PHASE3_BACKEND_URL` is server-side only — never in `NEXT_PUBLIC_*`
- [x] JWT token forwarded via `Authorization` header (not query param or body)
- [x] No API keys or model credentials stored in frontend
- [x] Input sanitised by React's JSX rendering (XSS-safe by default)
- [x] Empty message check prevents blank requests
- [x] User can only chat as themselves — `user_id` sourced from `useAuth()`, not user input

---

## Testing Scenarios

| # | Scenario | Expected |
|---|----------|---------|
| T1 | Send "List my tasks" as authenticated user | AI response with task list appears in ≤30s |
| T2 | Reload dashboard after conversation | Prior messages visible; same `conversation_id` used |
| T3 | Backend returns 500 | Error message + Retry button shown |
| T4 | Backend returns 404 (stale ID) | New conversation started transparently |
| T5 | Press Send with empty input | Button disabled; no request sent |
| T6 | Resize window to 320px | Drawer full-width; task list accessible after close |
| T7 | AI response includes tool call | ToolCallCard visible below assistant message |
| T8 | Send message while previous in flight | Send disabled; second message queued after first |

---

## Quickstart (local development)

```bash
# 1. Start Phase-3 backend
cd phase-3
source ../../venv/bin/activate
uvicorn src.main:app --port 8001 --reload

# 2. Add env variable
echo "PHASE3_BACKEND_URL=http://localhost:8001" >> phase-2/frontend/.env.local

# 3. Start Phase-2 frontend
cd phase-2/frontend
npm run dev

# 4. Open http://localhost:3000 → Sign in → Dashboard
# 5. Click 💬 Chat button in Navbar
# 6. Type "List my tasks" and press Enter
```
