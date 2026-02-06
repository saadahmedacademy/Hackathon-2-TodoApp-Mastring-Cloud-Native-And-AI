---
name: backend-skill
description: Build and maintain backend REST APIs, handle request/response validation, and connect application logic to the database.
---

# Backend Skill

## Instructions

1. **Route Generation**
   - Design RESTful API endpoints
   - Use clear, consistent URL structures
   - Map HTTP methods correctly to actions
   - Group routes by resource responsibility

2. **Request Handling**
   - Validate incoming requests using explicit schemas
   - Reject malformed or unauthorized requests early
   - Normalize input before passing to domain logic
   - Avoid trusting client-provided state

3. **Response Handling**
   - Return structured, predictable responses
   - Use correct HTTP status codes
   - Handle success and error cases explicitly
   - Avoid leaking internal implementation details

4. **Database Connection**
   - Interact with the database through repositories or ORM layers
   - Keep database access out of route handlers when possible
   - Handle transaction boundaries safely
   - Prevent N+1 queries and inefficient access patterns

--------------------------------------------------
BEST PRACTICES
--------------------------------------------------

- Keep route handlers thin
- Separate API, domain, and persistence layers
- Validate all inputs and outputs
- Prefer explicit schemas over implicit behavior
- Fail fast and fail safely

--------------------------------------------------
COMMON PITFALLS TO AVOID
--------------------------------------------------

- Business logic inside route handlers
- Missing or weak request validation
- Inconsistent response formats
- Incorrect or ambiguous HTTP status codes
- Tight coupling between API and database models

--------------------------------------------------
EXAMPLE FLOW (CONCEPTUAL)
--------------------------------------------------

Request:
Client → Validate Request → Auth Check → Domain Logic → DB Access → Response

--------------------------------------------------
SUCCESS CRITERIA
--------------------------------------------------

- API behavior is deterministic and testable
- Requests and responses are fully validated
- Database interactions are safe and efficient
- Backend layer is cleanly replaceable or extendable
- Backend supports future AI and agent-based access

