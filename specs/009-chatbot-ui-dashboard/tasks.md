# Tasks: Chatbot UI in Todo Dashboard

**Feature**: 009-chatbot-ui-dashboard
**Input**: Design documents from `/specs/009-chatbot-ui-dashboard/`
**Branch**: 007-refactor-jwt-secret
**Generated**: 2026-02-16
**Prerequisites**: plan.md ✅ spec.md ✅ data-model.md ✅ contracts/ ✅ research.md ✅

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create all new directories and foundational files for the chatbot feature.

- [x] T001 Create directory `phase-2/frontend/src/components/chat/`
- [x] T002 Create directory `phase-2/frontend/src/services/`
- [x] T003 Create directory `phase-2/frontend/src/app/api/chat/`
- [x] T004 Add `PHASE3_BACKEND_URL=http://localhost:8001` to `phase-2/frontend/.env.local` (create if not exists)

**Checkpoint**: Directory structure ready — implementation can begin.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Types, proxy route, and service layer — required by ALL user stories.

**⚠️ CRITICAL**: All user story work depends on this phase being complete.

- [x] T005 [P] Create TypeScript chat types (ChatMessage, ToolCallSummary, ChatState, ChatRequest, ChatApiResponse) in `phase-2/frontend/src/types/chat.ts`
- [x] T006 [P] Create Next.js server-side proxy route that forwards POST requests to Phase-3 backend using `PHASE3_BACKEND_URL` env var and passes Authorization header through in `phase-2/frontend/src/app/api/chat/route.ts`
- [x] T007 Create chat API service function `sendChatMessage(userId, message, conversationId, token)` that calls `POST /api/chat` proxy with Authorization header and typed error handling in `phase-2/frontend/src/services/chatService.ts`

**Checkpoint**: Foundation ready — user story implementation can begin.

---

## Phase 3: User Story 1 — Send a Chat Message from Dashboard (Priority: P1) 🎯 MVP

**Goal**: Authenticated user can open a chat drawer in the dashboard, type a message, send it to the AI agent, and see the response.

**Independent Test**: Sign in → open dashboard → click 💬 Chat button → type "List my tasks" → press Enter → verify AI response appears within 30 seconds.

### Implementation for User Story 1

- [x] T008 [P] [US1] Create `useChat` hook with `messages`, `conversationId`, `loading`, `error` state; implement `sendMessage(text)` that appends user message optimistically, calls `chatService.sendChatMessage`, updates state with response, and sets `loading` flag in `phase-2/frontend/src/hooks/useChat.ts`
- [x] T009 [P] [US1] Create `ChatInput` component with auto-resizing textarea (max 3 rows), Send button disabled when `value.trim() === ''` or `loading === true`, submit on Enter (Shift+Enter = newline), clears input after submit in `phase-2/frontend/src/components/chat/ChatInput.tsx`
- [x] T010 [P] [US1] Create `TypingIndicator` component with three animated bouncing dots (Tailwind `animate-bounce` with staggered delays), rendered only when `loading === true` in `phase-2/frontend/src/components/chat/TypingIndicator.tsx`
- [x] T011 [P] [US1] Create `MessageBubble` component: user messages right-aligned with primary color background, assistant messages left-aligned with muted background, timestamp in small text below content, in `phase-2/frontend/src/components/chat/MessageBubble.tsx`
- [x] T012 [US1] Create `MessageList` component: `overflow-y-auto` scrollable container rendering `MessageBubble` for each message, `useEffect` with `scrollIntoView` on messages change for auto-scroll in `phase-2/frontend/src/components/chat/MessageList.tsx`
- [x] T013 [US1] Create `ChatContainer` component that connects to `useChat()` hook, renders `MessageList` on top, `TypingIndicator` (conditional), and `ChatInput` fixed at bottom in a full-height flex column in `phase-2/frontend/src/components/chat/ChatContainer.tsx`
- [x] T014 [US1] Create `ChatDrawer` component: fixed-position right-side overlay (`z-50`), `w-full sm:w-96`, slide animation using Tailwind `transform transition-transform duration-300 translate-x-full` → `translate-x-0`, close button (✕) and backdrop click to close, renders `ChatContainer` inside in `phase-2/frontend/src/components/chat/ChatDrawer.tsx`
- [x] T015 [US1] Add `chatOpen` state and `ChatDrawer` to dashboard layout; render drawer outside `<main>` at root div level in `phase-2/frontend/src/app/dashboard/layout.tsx`
- [x] T016 [US1] Add 💬 Chat toggle button to right side of Navbar that calls `onChatToggle` prop to open/close the drawer in `phase-2/frontend/src/components/layout/Navbar.tsx`

**Checkpoint**: User Story 1 complete — chat drawer opens, message sends, AI response displays. Verify independently.

---

## Phase 4: User Story 2 — Resume a Previous Conversation (Priority: P2)

**Goal**: When a user returns to the dashboard, their prior conversation is restored from `localStorage` and continues with AI context intact.

**Independent Test**: Send "Add a task for testing" → reload the page → verify prior messages appear → send "What did I just ask you to do?" → verify AI references prior message.

### Implementation for User Story 2

- [x] T017 [US2] Add `localStorage` read on mount in `useChat` hook: read `chat_conversation_id_{userId}` key → set `conversationId` state; add write-to-localStorage whenever `conversationId` is updated; import `useAuth` to get `userId` in `phase-2/frontend/src/hooks/useChat.ts`
- [x] T018 [US2] Add 404-recovery logic in `sendMessage` in `useChat` hook: when backend returns 404 (stale `conversation_id`), clear `localStorage` key, reset `conversationId` to `null`, and automatically retry with `conversation_id: null` in `phase-2/frontend/src/hooks/useChat.ts`

**Checkpoint**: User Story 2 complete — conversation_id persists across reloads; stale IDs recovered automatically.

---

## Phase 5: User Story 3 — Tool Call Summary Visibility (Priority: P3)

**Goal**: When the AI agent executes a tool (e.g., adds or deletes a task), the chat UI shows a collapsible summary card below the AI message indicating which tool was called and its outcome.

**Independent Test**: Send "Delete my oldest task" → verify AI response includes a collapsible card showing "🔧 Tool used: delete_task — Task deleted successfully."

### Implementation for User Story 3

- [x] T019 [US3] Create `ToolCallCard` component using native `<details>/<summary>` HTML; summary line: `🔧 Tool used: {toolName}`; expanded section shows `input` (if present) and `outcome`; styled with Tailwind: bordered, rounded, muted background, `text-sm` in `phase-2/frontend/src/components/chat/ToolCallCard.tsx`
- [x] T020 [US3] Update `MessageList` to render `ToolCallCard` below each `MessageBubble` where `message.toolCalls` is present and non-empty in `phase-2/frontend/src/components/chat/MessageList.tsx`
- [x] T021 [US3] Update `useChat` hook's response mapper to extract `tool_calls` from backend response and map to `ToolCallSummary[]` on each assistant message in `phase-2/frontend/src/hooks/useChat.ts`

**Checkpoint**: All 3 user stories complete — send message, resume conversation, tool call summaries all independently working.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, UX polish, security hardening, deployment readiness.

- [x] T022 [P] Add inline error message display (red tinted `MessageBubble` with `isError: true`) and Retry button that calls `retry()` from `useChat` when `error !== null` in `phase-2/frontend/src/components/chat/ChatContainer.tsx`
- [x] T023 [P] Add `AbortController` timeout (30s) to `chatService.sendChatMessage` to prevent zombie requests; throw typed `ChatTimeoutError` on abort in `phase-2/frontend/src/services/chatService.ts`
- [x] T024 [P] Add 401 handling in `chatService`: when backend returns 401, throw `ChatAuthError` so `useChat` can redirect to `/signin` via `useRouter` in `phase-2/frontend/src/services/chatService.ts`
- [x] T025 Add `PHASE3_BACKEND_URL` as server-side environment variable in Vercel dashboard (document in `phase-2/frontend/.env.example` with placeholder value, never `NEXT_PUBLIC_` prefix) in `phase-2/frontend/.env.example`
- [x] T026 [P] Validate `PHASE3_BACKEND_URL` is set on startup in the proxy route; return 503 with descriptive error if missing in `phase-2/frontend/src/app/api/chat/route.ts`
- [x] T027 Run manual smoke test per quickstart steps: start Phase-3 backend → start Phase-2 frontend → sign in → open chat → send "List my tasks" → verify response appears

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
  └── Phase 2 (Foundational) — BLOCKS all user stories
        ├── Phase 3 (US1 - Send Message) 🎯 MVP
        │     └── Phase 4 (US2 - Resume Conversation)
        │           └── Phase 5 (US3 - Tool Call Summary)
        └── Phase 6 (Polish) — after all stories complete
```

### Task Dependencies Within Phases

```
T005, T006 [P] — run together (different files)
T007        — after T005 (imports types)

T008        — after T007 (imports chatService)
T009, T010, T011 [P] — run together (independent components)
T012        — after T011 (renders MessageBubble)
T013        — after T008, T012 (uses useChat + MessageList)
T014        — after T013 (wraps ChatContainer)
T015        — after T014 (renders ChatDrawer)
T016        — after T015 (calls toggle from layout)

T017, T018  — update T008's file (sequential)

T019        — new file, independent
T020        — after T019 (renders ToolCallCard)
T021        — updates T008's hook (after T020)

T022–T027 [P] — mostly independent polish tasks
```

### Parallel Opportunities

```bash
# Phase 2 — run in parallel:
Task: "Create types in src/types/chat.ts"         (T005)
Task: "Create proxy route in app/api/chat/route.ts" (T006)

# Phase 3 — run in parallel after T008:
Task: "Create ChatInput.tsx"       (T009)
Task: "Create TypingIndicator.tsx" (T010)
Task: "Create MessageBubble.tsx"   (T011)

# Phase 6 — run in parallel:
Task: "Add error display + Retry"  (T022)
Task: "Add AbortController timeout" (T023)
Task: "Add 401 handling"           (T024)
Task: "Add env var validation"     (T026)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T004)
2. Complete Phase 2: Foundational (T005–T007)
3. Complete Phase 3: User Story 1 (T008–T016)
4. **STOP and VALIDATE**: Open chat drawer, send a message, see AI response
5. Deploy to Vercel if validated

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. User Story 1 → **Chat works** → Demo/Deploy (MVP!)
3. User Story 2 → **Conversations persist** → Demo/Deploy
4. User Story 3 → **Tool actions visible** → Demo/Deploy
5. Polish → Production hardened

---

## Task Summary

| Phase | Tasks | Parallelizable | Story |
|-------|-------|---------------|-------|
| Phase 1: Setup | T001–T004 | — | — |
| Phase 2: Foundational | T005–T007 | T005, T006 | — |
| Phase 3: US1 (Send Message) | T008–T016 | T009, T010, T011 | US1 |
| Phase 4: US2 (Resume Conv.) | T017–T018 | — | US2 |
| Phase 5: US3 (Tool Calls) | T019–T021 | T019 | US3 |
| Phase 6: Polish | T022–T027 | T022, T023, T024, T026 | — |
| **Total** | **27 tasks** | **10 parallelizable** | **3 stories** |

**New files**: 9 (`chat.ts`, `route.ts`, `chatService.ts`, `useChat.ts`, `ChatDrawer.tsx`, `ChatContainer.tsx`, `MessageList.tsx`, `MessageBubble.tsx`, `ToolCallCard.tsx`, `ChatInput.tsx`, `TypingIndicator.tsx`)
**Modified files**: 2 (`dashboard/layout.tsx`, `Navbar.tsx`)
