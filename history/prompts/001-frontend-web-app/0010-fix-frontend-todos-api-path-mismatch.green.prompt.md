---
id: 0010
title: Fix frontend Todos API path mismatch
stage: green
date: 2026-02-09
surface: agent
model: gemini-1.5-flash
feature: 001-frontend-web-app
branch: main
user: 
command: 
labels: []
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - phase-2/frontend/src/lib/api.ts
tests_yaml: |
  - N/A (requires manual testing with running application)
prompt_text: |
  Task: Fix frontend Todos API path mismatch

  Current state:
  - Authentication flow is correct
  - Token is stored in localStorage after login
  - Dashboard loads successfully
  - Todos page calls GET /todos
  - FastAPI backend does NOT expose /todos
  - Backend exposes GET /api/tasks

  Requirements:
  1. Locate all frontend API calls using /todos
     (likely in src/lib/api.ts, todos service, or TodosPage component)
  2. Replace /todos with /api/tasks
  3. Ensure Authorization header is preserved
  4. Ensure empty todo list is handled gracefully (render empty state, not error)
  5. Do NOT modify backend code
  6. Do NOT change auth logic

  Acceptance Criteria:
  - GET /api/tasks returns 200 OK
  - Empty todos render without error
  - No 404 errors in backend logs
  - Token remains intact
  - Create / update / delete todos continue to work

  Output:
  - Updated frontend API code snippets
  - List of files changed
  - Confirmation that no /todos calls remain
response_text: |
  I have completed the task.

  **Files changed:**
  *   `/home/saadahmed/hk-2-project/phase-2/frontend/src/lib/api.ts`

  **Confirmation:**
  All frontend API calls that were using `/todos` have been updated to `/api/tasks`. The remaining instances of `/todos` are for UI routing and are outside the scope of this task.
outcome: ""
evaluation: ""
---