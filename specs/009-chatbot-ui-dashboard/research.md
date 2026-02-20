# Research: Chatbot UI in Todo Dashboard

**Feature**: 009-chatbot-ui-dashboard
**Date**: 2026-02-16
**Branch**: 007-refactor-jwt-secret

---

## Decision 1: Chat UI Placement (Side Drawer)

**Decision**: Implement as a **floating side drawer** that slides in from the right edge of the dashboard.

**Rationale**:
- Dashboard layout uses `flex` with Navbar + Sidebar + `<main>` area. A drawer overlay preserves all existing layout without restructuring.
- Floating widget would obstruct the task list on small screens (320px).
- Modal would block the entire dashboard, preventing multi-tasking.
- Embedded panel (split layout) would require restructuring the main content area and squeeze the task list.
- Side drawer is the industry-standard pattern for supplementary panels (GitHub Copilot Chat, VS Code, Slack) and best satisfies FR-001 (no obscuring of task list) and FR-014 (responsive).

**Alternatives considered**:
| Option | Verdict | Reason |
|--------|---------|--------|
| Floating widget (bottom-right FAB) | Rejected | Covers content on mobile; no message history visible |
| Modal dialog | Rejected | Blocks full screen; interrupts workflow |
| Embedded panel (split) | Rejected | Requires layout refactor; squeezes task list on small screens |
| Side drawer (chosen) | ✅ Accepted | Overlay, preserves layout, dismissible, pattern users know |

---

## Decision 2: conversation_id Persistence

**Decision**: Store in `localStorage` under the key `chat_conversation_id_{user_id}`.

**Rationale**:
- `localStorage` survives page reloads and tab restores (satisfies FR-007, SC-002).
- Keyed by `user_id` ensures isolation between multiple users on same device.
- `sessionStorage` discarded on tab close — would not satisfy SC-002.
- Cookie storage adds complexity and server-side considerations not needed here.

---

## Decision 3: API Communication Pattern

**Decision**: Direct `fetch` calls from the client component to the Phase-3 backend URL stored in a **server-side env variable proxied via a Next.js API route**.

**Rationale**:
- Phase-3 backend URL must NOT be exposed to the browser (FR-012, FR-013).
- A Next.js API route at `app/api/chat/route.ts` acts as a thin proxy — receives the request from the browser, attaches no additional secrets (the Phase-3 backend validates the JWT), and forwards to `PHASE3_BACKEND_URL`.
- This keeps the env variable server-side only and works on Vercel with zero additional infrastructure.
- Satisfies FR-012 and FR-013 completely.

**Proxy route**: `POST /api/chat` (Next.js) → forwards to `${PHASE3_BACKEND_URL}/api/{user_id}/chat`

---

## Decision 4: Message Queuing

**Decision**: Single in-flight request lock — the Send button is disabled while a request is in progress.

**Rationale**:
- Prevents race conditions from rapid repeated submissions.
- Simple to implement with `loading` boolean in `useChat` hook.
- Satisfies edge case: "multiple rapid messages sent → sequential queue."

---

## Decision 5: Tool Call Summary Rendering

**Decision**: Render tool call summaries as collapsible `<details>` cards below the AI message bubble.

**Rationale**:
- `<details>/<summary>` is native HTML, no library needed, accessible by default.
- Collapsed by default keeps the chat clean; expandable on demand.
- Satisfies FR-010 (visually distinct) and SC-006.

---

## Resolved Unknowns

| Unknown | Resolution |
|---------|-----------|
| Phase-3 backend URL | Configured via `PHASE3_BACKEND_URL` env var (server-side only) |
| Auth token forwarding | JWT from `useAuth` state → sent as `Authorization: Bearer` in proxy route request |
| CORS | Not an issue — Next.js proxy route calls backend server-to-server |
| Existing auth context shape | `useAuth()` returns `state.user.id` and token via `apiClient._accessToken` |
| Backend response shape | `{ conversation_id: string, messages: [], tool_calls?: [] }` confirmed in chat.py |
