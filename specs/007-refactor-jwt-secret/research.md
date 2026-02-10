# Research: Refactor JWT Secret

**Decision**: The primary decision is to replace `AUTH_SECRET_KEY` with `BETTER_AUTH_SECRET` across the `phase-2/src` backend to centralize and enhance JWT verification.

**Rationale**: This refactoring improves security by standardizing the secret key used for JWTs, making management and potential rotation easier. It also addresses the risk of using inconsistent or outdated authentication secrets.

**Alternatives Considered**:
-   *Leaving `AUTH_SECRET_KEY` as is*: Rejected due to security and maintenance concerns.
-   *Implementing a more complex secret management system (e.g., HashiCorp Vault integration)*: Considered overkill for the immediate scope, which focuses on a direct replacement and configuration via environment variables. This could be a future enhancement.

## Detailed Research Findings (based on explicit plan)

The implementation will follow a clear set of steps to ensure a smooth transition:

1.  **Identification**: All occurrences of `AUTH_SECRET_KEY` within the `phase-2/src` directory will be identified.
2.  **Replacement**: Identified `AUTH_SECRET_KEY` instances will be replaced with `BETTER_AUTH_SECRET`.
3.  **Configuration Update (`auth/config.py`)**: `phase-2/src/auth/config.py` will be modified to source `JWT_SECRET_KEY` from the `BETTER_AUTH_SECRET` environment variable, including a robust fallback.
4.  **Middleware Adjustment (`middleware/auth.py`)**: `phase-2/src/middleware/auth.py` will be updated to correctly utilize the newly configured `JWT_SECRET_KEY` for all JWT verification processes.
5.  **Modification Tracking**: A record of all modified files will be maintained.
6.  **Scope Verification**: A final check will be performed to ensure that no unintended changes have affected frontend components or public variables.
