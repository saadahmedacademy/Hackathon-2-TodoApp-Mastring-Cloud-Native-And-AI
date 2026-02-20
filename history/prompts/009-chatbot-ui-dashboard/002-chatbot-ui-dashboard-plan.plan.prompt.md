---
id: 002
title: Chatbot UI Dashboard Plan
stage: plan
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 009-chatbot-ui-dashboard
branch: 007-refactor-jwt-secret
user: saadahmed
command: /sp.plan
labels: ["chatbot","frontend","dashboard","plan","phase-2","phase-3","side-drawer","useChat"]
links:
  spec: specs/009-chatbot-ui-dashboard/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-chatbot-ui-dashboard/plan.md
  - specs/009-chatbot-ui-dashboard/research.md
  - specs/009-chatbot-ui-dashboard/data-model.md
  - specs/009-chatbot-ui-dashboard/contracts/chat-api.md
tests:
  - none (planning phase)
---

## Prompt

Phase A – UI Integration: Decide chatbot UX style (floating widget recommended), Create components/chat/, Add ChatContainer, MessageList, ChatInput.
Phase B – State Layer: Create useChat hook, Maintain conversation_id, Add retry mechanism, Add error boundary.
Phase C – API Integration: Create chatApi.ts, Connect to /api/{user_id}/chat, Ensure auth token forwarding if required.
Phase D – Backend Connection: Confirm Phase-3 endpoint is accessible, Ensure CORS configured, Validate environment variables on Vercel.
Phase E – UX & Enhancement: Add typing indicator, Add tool call collapsible panel, Add auto-scroll, Add conversation resume logic.
Phase F – Production Hardening: Add input validation, Add rate limiting (backend), Add error normalization, Add logging.
Phase G – Deployment: Test locally, Test staging, Deploy to Vercel, Monitor logs, Performance check.

## Response snapshot

Generated complete implementation plan for `009-chatbot-ui-dashboard` (Chatbot UI in Phase-2 Dashboard).

**Artifacts created:**
- `specs/009-chatbot-ui-dashboard/plan.md` — Full implementation plan (phases A–F + deployment)
- `specs/009-chatbot-ui-dashboard/research.md` — Research decisions (UX placement, persistence, proxy pattern)
- `specs/009-chatbot-ui-dashboard/data-model.md` — TypeScript types for ChatMessage, ToolCallSummary, ChatState
- `specs/009-chatbot-ui-dashboard/contracts/chat-api.md` — API contract for Next.js proxy route + Phase-3 backend

**Key architectural decisions:**
- UX: Side drawer (not floating widget) — preserves task list, no layout restructuring, industry-standard pattern
- Proxy: Next.js API route `app/api/chat/route.ts` — keeps PHASE3_BACKEND_URL server-side only
- State: `useChat` hook with localStorage persistence of `conversation_id` keyed by `user_id`
- Tool calls: Rendered as collapsible `<details>` cards using native HTML (no extra library)
- 9 new files, 2 modified files (dashboard layout + Navbar)

**Constitution**: All 5 principles PASS.

## Outcome

- ✅ Impact: Full implementation plan ready for /sp.tasks
- 🧪 Tests: 8 test scenarios defined in plan.md
- 📁 Files: plan.md, research.md, data-model.md, contracts/chat-api.md
- 🔁 Next prompts: /sp.tasks 009-chatbot-ui-dashboard → /sp.implement
- 🧠 Reflection: Side drawer chosen over floating widget — avoids content obstruction on mobile; proxy route pattern is the cleanest Vercel-compatible way to hide backend URL

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): constitution check — all PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): /sp.tasks to generate actionable implementation tasks
