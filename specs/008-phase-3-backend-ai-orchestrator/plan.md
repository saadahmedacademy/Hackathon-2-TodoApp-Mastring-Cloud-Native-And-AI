# Implementation Plan: Phase 3 Backend AI Orchestrator

**Branch**: `007-refactor-jwt-secret` | **Date**: February 12, 2026 | **Spec**: specs/008-phase-3-backend-ai-orchestrator/spec.md
**Input**: Feature specification from `/specs/008-phase-3-backend-ai-orchestrator/spec.md`

## Summary

This plan outlines the implementation for the Phase 3 Backend AI Orchestrator service. This service will enable AI-driven chat functionality and task management through a new FastAPI backend. It will integrate with OpenAI Agents SDK and the Official MCP SDK, connecting to an existing Neon PostgreSQL database for persistence of Conversation, Message, and shared Task data. The service will expose a stateless `POST /api/{user_id}/chat` endpoint and MCP tool endpoints, following a layered architecture similar to Phase 2.

## Technical Context

**Language/Version**: Python 3.10+ (consistent with Phase 2)
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, httpx (for external API calls), alembic (for migrations)
**Storage**: Existing Neon PostgreSQL database
**Testing**: pytest (for unit and integration tests), test containers (for integration tests with PostgreSQL if needed)
**Target Platform**: Linux server (containerized deployment is assumed for future phases)
**Project Type**: Backend service (FastAPI)
**Performance Goals**:
- `POST /api/{user_id}/chat` returns valid AI agent response within 500ms for 95% of requests.
- All task management API calls (add, list, complete, delete, update) complete within 200ms for 95% of requests.
**Constraints**:
- Must be fully stateless (server holds no memory between requests).
- Must operate under the `/phase-3` directory.
- Must use existing Neon DB.
- Must share the `Task` table with Phase 2.
- No business logic embedded directly in AI prompts.
**Scale/Scope**: Supports multiple concurrent user conversations and task operations. Initial deployment targets typical web application load.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Phase-First Correctness**: The service will be built as a complete, stable, and usable independent phase. No premature optimization.
- [x] **Simplicity Before Scale**: Prefer clear, readable code. Use established patterns.
- [x] **Clean Evolution**: The design allows for extension. Domain logic (models, services) is intended to be portable.
- [x] **Deterministic Behavior**: Stateless request cycles and persistent storage ensure deterministic behavior.
- [ ] **Human-Centered UX (even in CLI)**: This applies primarily to the CLI/API interface. API error messages will be clear.
- [x] **Phase-Specific Standards**: Adheres to Python 3.10+, FastAPI, SQLModel, Neon DB. Integrates OpenAI Agents SDK, Official MCP SDK as specified for Phase III.
- [x] **Constraints and Quality Standards**: Python >= 3.10. Consistent with Phase 2 patterns. No vendor lock-in for core logic.

## Project Structure

### Documentation (this feature)

```text
specs/008-phase-3-backend-ai-orchestrator/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-3/
├── src/
│   ├── api/                # FastAPI routers and endpoint definitions
│   ├── models/             # SQLModel definitions for Conversation, Message, Task
│   ├── repositories/       # Database interaction logic
│   ├── services/           # Business logic, orchestrating repositories and agents
│   ├── db/                 # Database connection, session management, migration utilities
│   ├── utils/              # General utility functions
│   ├── agents/             # AI agent definitions and configurations
│   └── mcp/                # MCP tool registration and execution logic
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── alembic/                # Alembic migration scripts
├── alembic.ini             # Alembic configuration
├── config.py               # Application configuration (e.g., database URL, API keys)
├── requirements.txt        # Python dependencies
└── README.md
```

**Structure Decision**: The chosen structure mirrors the clean layering pattern of Phase 2, adapted for the new backend service under `phase-3/src`, including dedicated directories for `agents/` and `mcp/` to accommodate AI orchestration and MCP tool integration.

## Phase 0: Outline & Research

**Research Tasks**:

- **R0-001: OpenAI Agents SDK & MCP SDK Integration Patterns**:
    - Research best practices for integrating OpenAI Agents SDK and Official MCP SDK within a FastAPI application, specifically focusing on stateless execution and tool binding.
    - Focus on how to manage agent state (if any) across stateless HTTP requests.
    - *Outcome*: `research.md` will contain recommended patterns for agent and MCP SDK integration.
- **R0-002: SQLModel & Neon DB Connection Management**:
    - Investigate optimal connection pooling and session management strategies for SQLModel with Neon PostgreSQL in a FastAPI context to ensure efficiency and scalability.
    - *Outcome*: `research.md` will detail the chosen connection strategy.
- **R0-003: Stateless Request Cycle for AI Agents**:
    - Research patterns for managing conversation history and agent execution within a stateless HTTP request, ensuring all necessary context is passed and persisted without server-side memory.
    - *Outcome*: `research.md` will outline the recommended approach for stateless agent interaction.

## Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete, resolving R0-001, R0-002, R0-003.

### Database Plan (`data-model.md`)

- **Conversation Model**:
    - Fields: `id` (PK), `user_id` (FK to a User table - assumed to exist in other service or managed by auth system, not defined here), `created_at`, `updated_at`.
- **Message Model**:
    - Fields: `id` (PK), `conversation_id` (FK to Conversation), `sender` (e.g., "user", "assistant"), `content`, `timestamp`.
- **Task Model**:
    - Re-use existing `Task` model from Phase 2. Ensure compatibility and define how `phase-3` will access and potentially extend it.
- **Migration Strategy**: Use Alembic for database schema migrations. Initial migration will create `Conversation` and `Message` tables and potentially adjust `Task` table access for `phase-3`.
- **Connection Reuse Strategy**: Implement SQLModel's session management, potentially using a dependency injection pattern for `db_session` in FastAPI endpoints, ensuring efficient connection pooling with Neon.

### API Contracts (`contracts/`)

- **`POST /api/{user_id}/chat`**:
    - **Request Body**:
        ```json
        {
          "conversation_id": "string | null", // Optional: if continuing an existing conversation
          "message": "string"
        }
        ```
    - **Response Body (Success 200)**:
        ```json
        {
          "conversation_id": "string",
          "user_message_id": "string",
          "assistant_message_id": "string",
          "assistant_response": "string",
          "tasks_performed": ["list of tasks performed by agent"] // Optional, if agent performs tasks
        }
        ```
    - **Response Body (Error 4xx/5xx)**:
        ```json
        {
          "detail": "string",
          "error_code": "string"
        }
        ```
- **MCP Tool Endpoints (e.g., `POST /api/tasks/{user_id}/add`, `GET /api/tasks/{user_id}/list`)**:
    - Define individual FastAPI endpoints for each MCP tool (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`), including request/response schemas. These will likely mirror the MCP SDK's tool definitions.

### Quickstart (`quickstart.md`)

- Outline environment setup (Python, `requirements.txt`).
- Database connection configuration (`.env` file).
- Instructions to run database migrations.
- Instructions to start the FastAPI server.
- Basic examples for calling the `POST /api/{user_id}/chat` endpoint and MCP tool endpoints (e.g., using `curl` or `httpx`).

### Agent Context Update

- Run `.specify/scripts/bash/update-agent-context.sh gemini` to add `FastAPI`, `SQLModel`, `OpenAI Agents SDK`, `Official MCP SDK`, `Neon PostgreSQL`, `Alembic` to the `GEMINI.md` context for Phase 3.

## Phase 2: Implementation (Not part of this plan document)

## Error Handling Plan

- **Tool Errors**: Implement custom exceptions for MCP tool failures (e.g., invalid tool arguments, tool execution errors). These should be caught and returned as structured API error responses.
- **DB Errors**: Catch specific SQLModel/SQLAlchemy exceptions (e.g., `IntegrityError`, `NoResultFound`) and map them to appropriate HTTP status codes and user-friendly messages.
- **Agent Errors**: Handle exceptions thrown by the OpenAI Agents SDK. This includes cases where the agent fails to generate a response, generates an invalid response, or encounters an internal error. Provide a graceful fallback or a generic error message.
- **User-friendly Response Fallback**: In case of critical errors during agent execution or response generation, provide a default, informative message to the user instead of a raw stack trace.
- **Centralized Error Handling**: Utilize FastAPI's exception handlers to provide consistent error responses across the API.

## Testing Strategy

- **Unit Testing**:
    - Use `pytest`.
    - Test individual functions in `repositories`, `services`, `utils`, `agents`, `mcp` in isolation.
    - Mock external dependencies (DB, OpenAI API, MCP SDK) using `unittest.mock`.
- **Integration Testing**:
    - Use `pytest` with `httpx.AsyncClient` for testing FastAPI endpoints.
    - Test the `POST /api/{user_id}/chat` endpoint from request to agent execution and database persistence.
    - Test MCP tool endpoints end-to-end.
    - **DB Mocking Strategy**: For tests requiring database interaction, consider:
        - Using an in-memory SQLite database for fast unit-like integration tests.
        - Using a test container (e.g., `testcontainers-python`) for a real PostgreSQL instance to ensure closer-to-production testing for critical paths.
- **Contract Testing**:
    - Implement tests to ensure API request/response schemas match defined contracts (e.g., using Pydantic validation).

## Security Plan

- **Auth Compatibility**: Design endpoints to be compatible with a future authentication layer (e.g., FastAPI dependency injection for user validation). For now, `user_id` will be passed in the URL.
- **`user_id` Validation**: Ensure `user_id` is validated (e.g., format, existence if possible through an external service) to prevent unauthorized access or data manipulation across users.
- **No Secret Leakage**: Ensure API keys, database credentials, and other sensitive information are loaded from environment variables (e.g., using Pydantic Settings) and never hardcoded or logged.
- **Environment Variable Management**: Document all required environment variables and provide clear instructions for their setup (e.g., in `config.py` and `.env.example`).
- **Input Validation**: Strict validation of all incoming API request data to prevent injection attacks and ensure data integrity.

## Risk Analysis

- **R1: Agent Reliability & Latency**:
    - Risk: AI agent responses may be slow or unreliable, impacting `POST /api/{user_id}/chat` performance and user experience.
    - Mitigation: Implement timeouts for agent calls. Provide clear error messages or fallback responses if the agent fails. Monitor agent performance metrics.
- **R2: Database Performance**:
    - Risk: Inefficient queries or high load could strain the Neon DB, affecting overall service responsiveness.
    - Mitigation: Optimize SQLModel queries. Implement proper indexing on `Conversation`, `Message`, and `Task` tables. Use connection pooling effectively.
- **R3: MCP Tool Complexity**:
    - Risk: Integrating and managing multiple MCP tools could become complex, leading to bugs or maintenance overhead.
    - Mitigation: Design a clear, modular structure for MCP tools. Ensure robust schema validation and error handling for each tool. Prioritize essential tools first.

## Refactoring Considerations

- **Agent Orchestration Logic**: As the number of agents and their complexity grows, consider abstracting the agent execution and tool selection logic into a more advanced orchestration layer.
- **Database Repository Layer**: Further abstract the repository layer to support multiple database backends (though not planned for this phase, consider future extensibility).
- **Service-to-Service Communication**: If `phase-3` needs to interact with other internal services beyond the database, consider introducing a dedicated client library or messaging pattern.

## Scalability Considerations

- **Stateless Design**: The core stateless design of the service ensures inherent horizontal scalability. Multiple instances of the FastAPI service can run behind a load balancer.
- **Database Scaling**: Reliance on Neon DB means database scaling is managed externally. Ensure efficient query patterns to minimize load on the DB.
- **Asynchronous Operations**: Utilize FastAPI's asynchronous capabilities (`async`/`await`) for I/O-bound operations (DB calls, external API calls to OpenAI) to maximize concurrency.
- **Connection Pooling**: Proper configuration of database connection pooling to avoid resource exhaustion under high load.
