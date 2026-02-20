# Feature Specification: Chatbot UI in Todo Dashboard

**Feature Branch**: `007-refactor-jwt-secret` (spec: `009-chatbot-ui-dashboard`)
**Created**: 2026-02-16
**Status**: Draft
**Input**: User description: "Implement Chatbot UI inside phase-2/frontend, displayed inside the Todo App dashboard, connected to POST /api/{user_id}/chat backend endpoint."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 – Send a Chat Message from Dashboard (Priority: P1)

A logged-in user opens their Todo Dashboard and sees a chat panel. They type a natural-language message (e.g., "Add a task to buy milk") and submit it. The AI agent processes the message, executes the appropriate action (task creation), and responds with a confirmation message. The conversation appears in the chat window.

**Why this priority**: This is the core value — users can manage their todo list through natural language without using the manual task UI.

**Independent Test**: Load the dashboard as an authenticated user, open the chat panel, type "List my tasks", submit, and verify an AI response appears within 30 seconds.

**Acceptance Scenarios**:

1. **Given** the user is on the dashboard and the chat panel is visible, **When** they type a message and press Send, **Then** a loading indicator appears, the message is sent to the backend, and the AI response is displayed in the chat window.
2. **Given** the user submits a message, **When** the backend returns an error or times out, **Then** an inline error message is shown with a Retry button.
3. **Given** the user has no prior conversation, **When** the first message is sent, **Then** a new `conversation_id` is created and persisted for the session.

---

### User Story 2 – Resume a Previous Conversation (Priority: P2)

A user who previously chatted with the AI returns to the dashboard. Their prior conversation is restored automatically using the stored `conversation_id`, so the AI has context of prior interactions.

**Why this priority**: Continuity of conversation significantly improves usability and AI accuracy for follow-up actions.

**Independent Test**: Start a conversation, reload the dashboard, verify prior messages appear and a follow-up message references prior context correctly.

**Acceptance Scenarios**:

1. **Given** the user has a stored `conversation_id` from a prior session, **When** they open the dashboard, **Then** the previous messages are displayed in the chat panel.
2. **Given** the user sends a follow-up message in a resumed conversation, **When** the backend receives the request with the existing `conversation_id`, **Then** the AI response reflects prior context.

---

### User Story 3 – Tool Call Summary Visibility (Priority: P3)

When the AI agent performs a tool action (e.g., creates or deletes a task) in response to a user message, the chat UI displays a brief summary of what tool was called and what it did, so the user understands what actions were taken on their behalf.

**Why this priority**: Transparency builds trust; users need to know when the AI is modifying their data.

**Independent Test**: Send "Delete my oldest task", verify the response includes a tool call summary like "Tool used: delete_task — Task deleted successfully."

**Acceptance Scenarios**:

1. **Given** the AI executes a tool call (e.g., `add_task`, `complete_task`), **When** the response is rendered, **Then** a visually distinct tool call summary card is displayed below the AI message.
2. **Given** the AI responds with no tool calls (e.g., answering a question), **Then** no tool call summary is shown.

---

### Edge Cases

- What happens when the user sends an empty message? → Submit button must be disabled; no request is sent.
- What happens when the network is unavailable mid-conversation? → Show an error with Retry; do not lose the typed message.
- What happens when `conversation_id` is stale or invalid on the backend? → Backend returns an error; frontend starts a new conversation transparently.
- What happens when multiple rapid messages are sent? → Each subsequent message waits for the prior response before being sent (sequential queue).
- What happens when the AI response is very long? → Chat messages scroll within the panel without overflowing the dashboard layout.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display a chat panel inside the existing Todo Dashboard layout without replacing or obscuring the task list.
- **FR-002**: The system MUST allow authenticated users to send text messages to the AI agent via the chat panel.
- **FR-003**: The system MUST communicate exclusively with the Phase-3 backend via `POST /api/{user_id}/chat`; no direct AI/Gemini calls from the frontend.
- **FR-004**: The system MUST include the authenticated user's `user_id` in all chat API requests.
- **FR-005**: The system MUST include `Authorization: Bearer <token>` in all chat API requests.
- **FR-006**: The system MUST maintain `conversation_id` state across messages within a session; a new conversation starts when none exists.
- **FR-007**: The system MUST persist `conversation_id` in browser storage so conversations resume on page reload.
- **FR-008**: The system MUST display a loading/typing indicator while awaiting an AI response.
- **FR-009**: The system MUST display an inline error message and Retry button when a chat request fails.
- **FR-010**: The system MUST render tool call summaries as visually distinct cards when the backend response includes `tool_calls`.
- **FR-011**: The system MUST disable the Send button when the input is empty or while a request is in flight.
- **FR-012**: The system MUST NOT expose API keys or backend credentials in the browser.
- **FR-013**: All environment variables used for backend communication MUST be server-side only (not prefixed with `NEXT_PUBLIC_` for sensitive values).
- **FR-014**: The chat UI MUST be responsive and function correctly on screen widths from 320px to 1920px.

### Key Entities

- **ChatMessage**: A single message in a conversation, with role (`user` | `assistant`), content text, optional tool call summary, and timestamp.
- **Conversation**: A session of messages identified by a `conversation_id` (UUID), linked to a user.
- **ToolCallSummary**: A structured record of an agent tool execution — tool name, input parameters (summarized), and outcome.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can send a message and receive an AI response within 30 seconds under normal network conditions.
- **SC-002**: Conversation history is restored on dashboard reload 100% of the time when a valid `conversation_id` is stored in the browser.
- **SC-003**: The chat panel does not disrupt the existing task list layout at any supported screen width.
- **SC-004**: Zero frontend errors caused by missing or expired API keys (all sensitive config remains server-side).
- **SC-005**: 95% of chat interactions display a meaningful AI response (not a generic error) when the backend is available.
- **SC-006**: Tool call summaries are shown for 100% of responses where `tool_calls` is present in the backend payload.

---

## Assumptions

- The Phase-3 backend `POST /api/{user_id}/chat` endpoint is already implemented and accessible via a configurable environment variable `PHASE3_BACKEND_URL`.
- The existing Phase-2 authentication context (`useAuth` / `AuthContext`) provides the current `user_id` and JWT token.
- The backend accepts `{ message: string, conversation_id: string | null }` and returns `{ conversation_id: string, messages: [], tool_calls?: [] }` as specified.
- The chat panel will be implemented as a **side drawer** (slides in from the right) toggled by a button in the dashboard header — chosen for best UX because it maximises task list visibility while keeping chat accessible without a full layout change.
- `conversation_id` will be stored in `localStorage` keyed by `user_id` so each user has an isolated conversation context.
- No streaming responses in this phase — the frontend waits for the full response before rendering.

---

## Out of Scope

- Streaming / server-sent event (SSE) responses
- Multi-conversation management (switching between conversations)
- File or image attachments
- Voice input
- Chatbot UI in any page other than the dashboard
- Any backend changes (Phase-3 backend is pre-built)
- Direct MCP server integration from the frontend
