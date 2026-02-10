# Quickstart: Refactor JWT Secret

This quickstart guide provides instructions for setting up your environment to work with the `BETTER_AUTH_SECRET` refactoring.

## Prerequisites

-   A running instance of the `phase-2` backend application.
-   Access to the environment configuration of the `phase-2` backend.

## Environment Setup

The core of this refactoring involves reading the JWT secret from an environment variable.

1.  **Set `BETTER_AUTH_SECRET` Environment Variable**:
    Ensure that the `BETTER_AUTH_SECRET` environment variable is set in the environment where the `phase-2` backend application runs. This variable should contain a strong, randomly generated secret key.

    *Example (for development/testing - NOT for production):*
    ```bash
    export BETTER_AUTH_SECRET="your_super_secret_jwt_key_here_replace_me_in_prod"
    ```
    *Note: In production environments, use a secure secret management system (e.g., Kubernetes Secrets, AWS Secrets Manager, Google Secret Manager) to manage this variable.*

2.  **Restart Backend Application**:
    After setting the environment variable, restart the `phase-2` backend application to ensure it picks up the new `BETTER_AUTH_SECRET` value.

## Verification

To verify that the refactoring is working correctly:

1.  Attempt to authenticate with the backend using existing credentials.
2.  Ensure that JWTs are still correctly generated and validated.
3.  Check backend logs for any warnings or errors related to JWT secret loading or verification.
    (FR-005: System MUST log an error if `BETTER_AUTH_SECRET` is not properly configured.)

This will confirm that the system is correctly using the `BETTER_AUTH_SECRET` for JWT operations.
