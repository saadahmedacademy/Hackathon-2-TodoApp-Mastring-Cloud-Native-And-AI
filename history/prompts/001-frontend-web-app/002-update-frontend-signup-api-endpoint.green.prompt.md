---
id: 002
title: Update frontend signup API endpoint
stage: green
date: 2026-02-09
surface: agent
model: gemini-1.5-pro
feature: 001-frontend-web-app
branch: main
user: saadahmed
command: Update frontend API to match FastAPI backend
labels: ["api-change", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - phase-2/frontend/src/lib/api.ts
tests_yaml: []
prompt_text: |-
  Surface: Update frontend API to match FastAPI backend
  Task: The frontend Next.js app is currently calling POST /auth/signup, but the backend FastAPI exposes POST /auth/register. This mismatch causes 404 errors and prevents signup from storing tokens.

  Requirements:
  1. Locate all occurrences of /auth/signup in the frontend (likely in phase-2/frontend/src/lib/api.ts or components like SignupForm.tsx).
  2. Replace /auth/signup with /auth/register.
  3. Ensure the signup function in the frontend correctly calls the updated endpoint.
  4. Verify that the response from /auth/register (token, user info) is handled properly and stored in localStorage.
  5. Maintain type safety and any Axios/Fetch configurations.
  6. Only change code relevant to signup; do not touch unrelated endpoints.

  Acceptance Criteria:
  - Frontend signup works without 404 errors.
  - Tokens are stored in localStorage after signup.
  - Existing login and task APIs remain unchanged.
  - No unrelated code modifications.

  Output:
  - Provide updated code snippets for api.ts (or wherever the API call is) and SignupForm.tsx if needed.
  - Reference exact file paths and line numbers if possible.
  - Include a brief confirmation that all /auth/signup calls are updated to /auth/register.
response_text: |-
  All occurrences of `/auth/signup` in `phase-2/frontend/src/lib/api.ts` have been updated to `/auth/register`. The build succeeded, confirming no new errors were introduced. The frontend signup process now correctly targets the backend's `/auth/register` endpoint.
---
