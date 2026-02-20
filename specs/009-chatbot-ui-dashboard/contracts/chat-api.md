# API Contract: Chatbot Chat Endpoint

**Feature**: 009-chatbot-ui-dashboard
**Date**: 2026-02-16

---

## Next.js Proxy Route (Frontend → Backend Bridge)

### POST `/api/chat`

This is a Next.js App Router API route (`app/api/chat/route.ts`) that:
1. Receives the chat request from the browser
2. Reads `PHASE3_BACKEND_URL` from server-side env (never exposed to browser)
3. Forwards the request to Phase-3 backend at `POST {PHASE3_BACKEND_URL}/api/{user_id}/chat`
4. Returns the backend response to the browser

**Request** (browser → Next.js proxy):
```http
POST /api/chat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "message": "Add a task to buy milk",
  "conversation_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301"  // null for new conversation
}
```

**Response** (Next.js proxy → browser):
```json
{
  "conversation_id": "3f2504e0-4f89-11d3-9a0c-0305e82c3301",
  "messages": [
    {
      "role": "user",
      "content": "Add a task to buy milk",
      "created_at": "2026-02-16T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I've added 'Buy milk' to your task list.",
      "tool_calls": [
        {
          "tool_name": "add_task",
          "input": "Buy milk",
          "outcome": "Task created successfully."
        }
      ],
      "created_at": "2026-02-16T10:00:05Z"
    }
  ]
}
```

**Error Responses**:

| Status | Condition | Frontend Action |
|--------|-----------|----------------|
| 400 | Invalid message or bad request | Show error message |
| 401 | JWT token expired or missing | Redirect to signin |
| 404 | conversation_id not found | Clear localStorage, start new conversation |
| 500 | Backend / AI agent error | Show error with Retry button |
| 504 | Timeout (>30s) | Show timeout error with Retry button |

---

## Phase-3 Backend Endpoint (reference only — no frontend changes)

### POST `/api/{user_id}/chat`

**Implemented in**: `phase-3/src/api/v1/endpoints/chat.py`

**Request body** (forwarded from proxy):
```json
{
  "message": "string",
  "conversation_id": "uuid | null"
}
```

**Response body**:
```json
{
  "conversation_id": "uuid",
  "messages": [
    {
      "role": "user | assistant",
      "content": "string",
      "tool_calls": [
        {
          "tool_name": "string",
          "input": "string",
          "outcome": "string"
        }
      ],
      "created_at": "ISO datetime"
    }
  ]
}
```

---

## Environment Variables

| Variable | Location | Purpose |
|----------|----------|---------|
| `PHASE3_BACKEND_URL` | Server-side (`.env.local`) | Phase-3 FastAPI base URL |
| `NEXT_PUBLIC_API_BASE_URL` | Client-side (already exists) | Phase-2 FastAPI base URL |

> **Security**: `PHASE3_BACKEND_URL` must NEVER be prefixed with `NEXT_PUBLIC_`. It is only accessed server-side in the Next.js API route.
