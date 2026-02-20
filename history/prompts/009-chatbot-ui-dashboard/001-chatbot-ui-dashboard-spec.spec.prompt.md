---
id: 001
title: Chatbot UI Dashboard Spec
stage: spec
date: 2026-02-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: 009-chatbot-ui-dashboard
branch: 007-refactor-jwt-secret
user: saadahmed
command: /sp.specify
labels: ["chatbot","frontend","dashboard","phase-2","phase-3","spec"]
links:
  spec: specs/009-chatbot-ui-dashboard/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-chatbot-ui-dashboard/spec.md
  - specs/009-chatbot-ui-dashboard/checklists/requirements.md
tests:
  - none
---

## Prompt

We are updating Phase-3 architecture.

Previous decision:
Chat UI was planned inside /phase-3/frontend.

New Decision:
Chatbot UI must now be implemented inside the existing Phase-2 Next.js frontend application and displayed inside the Todo App dashboard.

Working Git Branch:
Don't create a separate branch, work in current '007-refactor-jwt-secret' but create a new spec.

Important Context:
- Phase-2 Next.js app is deployed on Vercel.
- Phase-3 contains backend AI Agent implementation.
- Backend uses OpenAI Agents SDK configured with Gemini via OpenAI-compatible API.
- Neon PostgreSQL is already configured.
- We must NOT duplicate backend logic.
- Frontend must only communicate via API.
- No MCP usage.

OBJECTIVE: Implement Chatbot UI inside phase-2/frontend, displayed inside the Todo Dashboard page, connected to POST /api/{user_id}/chat. Backend logic remains inside Phase-3.

## Response snapshot

Created spec `009-chatbot-ui-dashboard` on branch `007-refactor-jwt-secret` (no new branch created).

**Files created:**
- `specs/009-chatbot-ui-dashboard/spec.md` — full feature specification
- `specs/009-chatbot-ui-dashboard/checklists/requirements.md` — quality checklist (all items pass)

**Key decisions captured in spec:**
- UX placement: **Side drawer** (slides in from right) — maximises task list visibility
- `conversation_id` persisted in `localStorage` keyed by `user_id`
- No streaming in this phase — full response before render
- 14 Functional Requirements defined (FR-001–FR-014)
- 6 measurable Success Criteria (SC-001–SC-006)
- 3 user stories (P1: send message, P2: resume conversation, P3: tool call summary)
- Out of scope: streaming, multi-conversation, voice, MCP from frontend

## Outcome

- ✅ Impact: Architecture decision formalised — Chat UI moves from phase-3/frontend into phase-2/frontend dashboard
- 🧪 Tests: No tests in spec phase; acceptance scenarios defined per user story
- 📁 Files: specs/009-chatbot-ui-dashboard/spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.plan 009-chatbot-ui-dashboard, then /sp.tasks, then /sp.implement
- 🧠 Reflection: Side drawer chosen over modal/embedded panel as best balance of screen real estate and accessibility on dashboard

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): requirements checklist — all PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): run /sp.clarify if UX placement needs stakeholder sign-off before planning
