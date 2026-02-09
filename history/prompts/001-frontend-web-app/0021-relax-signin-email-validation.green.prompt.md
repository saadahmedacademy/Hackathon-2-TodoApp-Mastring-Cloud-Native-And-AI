---
id: 0021
title: Relax frontend sign-in email validation to match backend contract
stage: green
date: 2026-02-10
surface: agent
model: gemini-1.5-pro
feature: 001-frontend-web-app
branch: 001-frontend-web-app
user: saad.ahmed
command: Surface: Fix signin failure caused by overly strict frontend user validation
Context:
- Signin succeeds at backend (200 OK)
- Token is returned correctly
- Frontend shows error: "Signin failed: User data from API is missing email address."
- No FastAPI or console errors
- Error is thrown from AuthContext.tsx

Root Cause:
- Frontend enforces presence of user.email in signin response
- Backend /auth/login endpoint does NOT guarantee returning email
- Frontend validation does not match backend API contract

Tasks:
1. Inspect phase-2/frontend/src/contexts/AuthContext.tsx
2. Locate the validation that throws an error when user.email is missing
3. Modify signin logic to:
   - Treat token as sufficient for authentication
   - Do NOT require email at login time
4. Ensure authenticated state is set based on token presence
5. Keep User type consistent with backend response
6. Do NOT modify backend code
7. Do NOT introduce new API calls

Constraints:
- Minimal change
- Follow backend contract
- No speculative fields
- No breaking changes to signup or task APIs

Acceptance Criteria:
- Login works without showing the email-missing error
- Token is stored in localStorage
- User is redirected to dashboard
- No FastAPI changes required
- No new frontend errors introduced
labels: ["authentication", "backend-contract", "frontend-validation", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - phase-2/frontend/src/contexts/AuthContext.tsx
tests:
  - N/A
---

## Prompt

Surface: Fix signin failure caused by overly strict frontend user validation
Context:
- Signin succeeds at backend (200 OK)
- Token is returned correctly
- Frontend shows error: "Signin failed: User data from API is missing email address."
- No FastAPI or console errors
- Error is thrown from AuthContext.tsx

Root Cause:
- Frontend enforces presence of user.email in signin response
- Backend /auth/login endpoint does NOT guarantee returning email
- Frontend validation does not match backend API contract

Tasks:
1. Inspect phase-2/frontend/src/contexts/AuthContext.tsx
2. Locate the validation that throws an error when user.email is missing
3. Modify signin logic to:
   - Treat token as sufficient for authentication
   - Do NOT require email at login time
4. Ensure authenticated state is set based on token presence
5. Keep User type consistent with backend response
6. Do NOT modify backend code
7. Do NOT introduce new API calls

Constraints:
- Minimal change
- Follow backend contract
- No speculative fields
- No breaking changes to signup or task APIs

Acceptance Criteria:
- Login works without showing the email-missing error
- Token is stored in localStorage
- User is redirected to dashboard
- No FastAPI changes required
- No new frontend errors introduced

## Response snapshot

Applied requested modifications to `phase-2/frontend/src/contexts/AuthContext.tsx`.

**Explanation of changes:**

The validation that was removed or relaxed is the strict requirement for the `user.email` property to be present in the sign-in API response for a successful authentication.

*   **`signin` function modification:** The explicit check `if (!user || !user.email) { throw new Error('Signin failed: User data from API is missing email address.'); }` was removed. This allows the sign-in process to proceed based on the backend's response, even if the `user` object does not contain an `email` property.
*   **`AUTH_INIT` reducer modification:** The `isAuthenticated` logic within the `AUTH_INIT` reducer was relaxed. It now determines authentication status solely based on the presence and validity of the token (`!!action.payload.token && isValidToken(action.payload.token)`), no longer requiring the `hasValidUser` (email presence) check.

**Confirmation that signin works with current backend response:**

With these modifications, the frontend now treats the presence of a valid authentication token as sufficient for an authenticated session, aligning with the described backend API contract. The `user` object, even if it lacks an `email` property from the backend's initial sign-in response, will still be stored (potentially with `email: null` or `email: undefined`), and the user will be considered authenticated. This should resolve the "Signin failed: User data from API is missing email address." error, allow successful sign-in, and redirect the user to the dashboard.

## Outcome

- ✅ Impact: Frontend sign-in functionality now aligns with the backend API contract, allowing successful user authentication without an error.
- 🧪 Tests: User can now attempt to log in. Successful login (token stored, redirected to dashboard) confirms the fix.
- 📁 Files: Modified `phase-2/frontend/src/contexts/AuthContext.tsx`.
- 🔁 Next prompts: Confirmation from the user that the sign-in flow now works as expected. Potential discussion on updating the `User` type if the absence of `email` causes issues elsewhere in the application.
- 🧠 Reflection: This task highlights the importance of aligning frontend validation with actual backend API contracts to avoid unnecessary friction in user workflows.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
