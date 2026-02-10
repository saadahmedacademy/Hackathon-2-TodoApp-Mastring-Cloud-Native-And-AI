# Feature Specification: Refactor JWT Secret

**Feature Branch**: `007-refactor-jwt-secret`  
**Created**: February 10, 2026  
**Status**: Draft  
**Input**: User description: "Replace AUTH_SECRET_KEY in backend with BETTER_AUTH_SECRET for Better Auth JWT verification. Ensure all files in phase-2/src using JWT_SECRET_KEY read from BETTER_AUTH_SECRET instead. Update auth/config.py and middleware/auth.py. Generate a list of all modified files."

## User Scenarios & Testing

### User Story 1 - Enhance Security by Centralizing JWT Secret Management (Priority: P1)

This story focuses on improving the security posture of the backend by ensuring that the JWT secret key used for authentication is consistently managed and referenced across all relevant modules. By replacing direct references to `AUTH_SECRET_KEY` with `BETTER_AUTH_SECRET`, we centralize the secret management, making it easier to update and audit, and reducing the risk of using outdated or insecure keys.

**Why this priority**: This is a critical security enhancement. Inconsistent secret management can lead to vulnerabilities. Centralizing it reduces attack surface and simplifies maintenance.

**Independent Test**: The system's authentication mechanisms can be fully tested to ensure JWTs are correctly signed and verified using the new `BETTER_AUTH_SECRET` without impacting other system functionalities.

**Acceptance Scenarios**:

1.  **Given** the backend services are running, **When** a user attempts to authenticate, **Then** the system MUST successfully verify the JWT using `BETTER_AUTH_SECRET`.
2.  **Given** the backend services are running, **When** a module in `phase-2/src` attempts to access the JWT secret, **Then** it MUST retrieve `BETTER_AUTH_SECRET` instead of `AUTH_SECRET_KEY`.
3.  **Given** the backend services are running, **When** `auth/config.py` is loaded, **Then** it MUST expose `BETTER_AUTH_SECRET` for JWT operations.
4.  **Given** the backend services are running, **When** `middleware/auth.py` processes an incoming request, **Then** it MUST use `BETTER_AUTH_SECRET` for JWT verification.

### Edge Cases

-   **What happens when `BETTER_AUTH_SECRET` is not configured?**: The system should fail gracefully, preventing authentication attempts and logging a critical error.
-   **How does the system handle rotation of `BETTER_AUTH_SECRET`?**: The system should support changing the secret without requiring code changes, ideally via environment variables or a secure configuration management system.

## Requirements

### Functional Requirements

-   **FR-001**: The system MUST use `BETTER_AUTH_SECRET` for all JWT signing and verification operations in the backend.
-   **FR-002**: All references to `AUTH_SECRET_KEY` within `phase-2/src` MUST be updated to `BETTER_AUTH_SECRET`.
-   **FR-003**: The `auth/config.py` file MUST be updated to define and expose `BETTER_AUTH_SECRET`.
-   **FR-004**: The `middleware/auth.py` file MUST be updated to utilize `BETTER_AUTH_SECRET` for JWT verification.
-   **FR-005**: The system MUST log an error if `BETTER_AUTH_SECRET` is not properly configured.

### Key Entities

-   **JWT (JSON Web Token)**: Represents a secure means of transmitting information between parties as a JSON object, signed using a secret.
-   **Authentication Secret**: A cryptographic key (`BETTER_AUTH_SECRET`) used to sign and verify JWTs, ensuring their integrity and authenticity.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: All JWT verification processes in the backend successfully use `BETTER_AUTH_SECRET` after the change, with no authentication failures due to secret mismatch.
-   **SC-002**: There are no remaining direct code references to `AUTH_SECRET_KEY` within `phase-2/src` that are used for JWT operations.
-   **SC-003**: The update to the authentication secret can be deployed and activated without requiring downtime or user re-authentication beyond standard JWT expiry.
-   **SC-004**: System logs clearly indicate the successful loading of `BETTER_AUTH_SECRET` and any failures to do so.