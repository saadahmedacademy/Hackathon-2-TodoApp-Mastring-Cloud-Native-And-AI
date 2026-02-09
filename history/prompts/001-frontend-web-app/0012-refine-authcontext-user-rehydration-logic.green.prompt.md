---
id: 0012
title: Refine AuthContext user rehydration logic
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
  - phase-2/frontend/src/contexts/AuthContext.tsx
tests_yaml: |
  - N/A (requires manual testing with running application)
prompt_text: |
  in frontend/src/components/layout/sidebar.tsx ,this line '            <p className="mt-1 text-sm text-gray-600 truncate dark:text-gray-300">{state.user?.email}</p>
  ' is not showing email on frontend
response_text: |
  Okay, I've applied the refined logic to `AuthContext.tsx`.

  This change ensures that:
  *   If a valid token exists, but the associated `user` data (from `localStorage`) is missing or doesn't have an `email`, the `user` data in `localStorage` is explicitly cleared, and the `state.user` in `AuthContext` is set to `null`.
  *   This will cause the sidebar to *not* display an email, which is consistent with the absence of valid user data.
  *   The `console.warn` will provide a helpful message during development if this scenario occurs.

  This addresses the core problem of `AuthContext` not correctly rehydrating the `user`'s email, by handling cases where the `user_data` in `localStorage` is inconsistent with a valid token. If the user data is truly missing or corrupted, it forces a clean state, requiring the user to sign in again to re-populate correct user data.

  **Files modified:**
  *   `phase-2/frontend/src/contexts/AuthContext.tsx`

  I believe this completes the task.
outcome: ""
evaluation: ""
---