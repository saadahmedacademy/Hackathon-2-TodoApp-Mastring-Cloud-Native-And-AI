---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill

## Instructions

1. **User Signup**
   - Accept validated user credentials (email/username + password)
   - Enforce strong password requirements
   - Hash passwords before storage
   - Prevent duplicate account creation

2. **User Signin**
   - Verify credentials securely
   - Protect against timing attacks
   - Return authentication tokens on success
   - Handle invalid credentials safely

3. **Password Security**
   - Use modern, adaptive hashing algorithms (e.g., bcrypt, argon2)
   - Never store or log plain-text passwords
   - Support future password rotation or reset flows

4. **JWT Token Handling**
   - Issue short-lived access tokens
   - Optionally support refresh tokens
   - Sign tokens securely
   - Validate token integrity and expiration on every request

5. **Better Auth Integration**
   - Integrate with Better Auth as an authentication provider
   - Treat Better Auth as an external identity layer
   - Map external identities to internal user records
   - Handle provider errors and fallback scenarios

--------------------------------------------------
SECURITY REQUIREMENTS
--------------------------------------------------

- Validate all inputs before processing
- Sanitize authentication-related data
- Use constant-time comparisons for secrets
- Do not leak authentication failure reasons
- Enforce least-privilege access

--------------------------------------------------
BEST PRACTICES
--------------------------------------------------

- Keep auth logic isolated from domain logic
- Centralize authentication and authorization checks
- Use explicit token validation middleware
- Rotate secrets without code changes
- Log auth events without sensitive data

--------------------------------------------------
COMMON PITFALLS TO AVOID
--------------------------------------------------

- Storing passwords in plain text
- Using weak or deprecated hashing algorithms
- Long-lived access tokens without rotation
- Trusting client-provided authentication state
- Mixing auth logic with business rules

--------------------------------------------------
EXAMPLE FLOW (CONCEPTUAL)
--------------------------------------------------

Signup:
User → Validate Input → Hash Password → Store User → Issue Token

Signin:
User → Validate Input → Verify Password → Issue Token

Protected Request:
Request → Validate JWT → Authorize User → Execute Action

--------------------------------------------------
SUCCESS CRITERIA
--------------------------------------------------

- Authentication flows are secure and deterministic
- Passwords are never exposed or persisted in plain text
- JWT tokens are correctly issued and validated
- Better Auth integration is clean and replaceable
- Auth layer is reusable across multiple phases

