# Implementation Plan: Phase-II Backend Core

**Branch**: `002-backend-core` | **Date**: 2026-02-02 | **Spec**: ../001-console-todo-app/spec.md
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a FastAPI backend that exposes task management APIs, persists data in Neon PostgreSQL, and reuses Phase-I domain logic via an adapter layer. The architecture implements all 5 Todo features as REST endpoints with multi-user support and proper data isolation through user ownership enforcement.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server (REST API)
**Project Type**: Web/backend (REST API)
**Performance Goals**: Support 100 concurrent users, <200ms response time
**Constraints**: Must reuse Phase-I domain logic without modification, enforce user ownership at data level
**Scale/Scope**: Multi-user support with proper data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Phase-First Correctness**: Architecture must allow reuse of Phase-I domain logic without modification
- **Simplicity Before Scale**: Use minimal dependencies (FastAPI, SQLModel) for this phase
- **Clean Evolution**: Design must allow domain logic to be portable across interfaces (CLI → API)
- **Phase-Specific Standards**: Follow Phase II standards (Next.js, FastAPI, SQLModel, Neon DB)
- **Deterministic Behavior**: API responses must be consistent and predictable
- **Multi-user Support**: Enforce user ownership at data level via user_id

## Project Structure

### Documentation (this feature)

```text
specs/002-backend-core/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase-2/
├── src/
│   ├── models/           # SQLModel database models
│   ├── services/         # Business logic services with adapter layer
│   ├── repositories/     # Database access layer
│   └── api/              # FastAPI route definitions
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt      # Python dependencies
```

**Structure Decision**: Phase-II backend follows clean architecture with separation of concerns. Models define database schema using SQLModel, repositories handle database operations, services contain business logic with adapter to reuse Phase-I domain logic, and API layer defines REST endpoints.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
