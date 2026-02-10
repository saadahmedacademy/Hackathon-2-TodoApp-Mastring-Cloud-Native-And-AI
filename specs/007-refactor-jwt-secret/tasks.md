# Tasks: Refactor JWT Secret

**Input**: Design documents from `/home/saadahmed/hk-2-project/specs/007-refactor-jwt-secret/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `phase-2/src/` (backend), `phase-2/frontend/src/` (frontend)

## Overview
This document outlines the tasks required to refactor the JWT secret key management in the backend, transitioning from `AUTH_SECRET_KEY` to `BETTER_AUTH_SECRET`. Tasks are organized by phases, focusing on independent testability and clear file paths.

## Task Dependencies

*   Phase 2 tasks depend on Phase 1 completion.
*   Phase 3 tasks depend on Phase 2 completion.
*   Final Phase tasks depend on Phase 3 completion.

## Parallel Execution Examples

Due to the sequential nature of identifying, replacing, and updating dependent files for a critical security mechanism, most tasks in this refactoring are sequential. Limited parallelization opportunities exist, primarily for verification steps that can be run concurrently once the core changes are in place.

## Implementation Strategy

The implementation will proceed incrementally, ensuring that each step is verified before moving to the next. The focus is on safety and correctness during the sensitive operation of refactoring an authentication secret.

---

## Phase 1: Setup

**Purpose**: Ensure the testing environment is ready.

- [x] T001 Ensure a robust testing environment is configured for the `phase-2` backend, capable of running authentication tests.

## Phase 2: Foundational

**Purpose**: Establish a baseline and prepare for core changes.

- [x] T002 Execute existing authentication tests in `phase-2/tests/` to establish a baseline of current JWT verification functionality.
- [x] T003 Capture a list of currently configured environment variables in the `phase-2` backend to identify if `AUTH_SECRET_KEY` is directly exposed.

## Phase 3: User Story 1 - Enhance Security by Centralizing JWT Secret Management [US1]

**Goal**: Successfully replace `AUTH_SECRET_KEY` with `BETTER_AUTH_SECRET` ensuring all JWT operations use the new secret and existing functionality remains intact.
**Independent Test**: The system's authentication mechanisms can be fully tested to ensure JWTs are correctly signed and verified using the new `BETTER_AUTH_SECRET` without impacting other system functionalities.

### Implementation for User Story 1

- [x] T004 [US1] Search for all occurrences of `AUTH_SECRET_KEY` within the `phase-2/src` directory, and document findings (e.g., log to a temporary file for review).
- [x] T005 [US1] Create a new environment variable `BETTER_AUTH_SECRET` with a strong, temporary secret value in the development environment (`quickstart.md` provides guidance). (Note: `BETTER_AUTH_SECRET_KEY` already present in `phase-2/.env`).
- [x] T006 [US1] Replace identified occurrences of `AUTH_SECRET_KEY` with `BETTER_AUTH_SECRET` in relevant files within `phase-2/src` (e.g., `phase-2/src/auth/config.py`, other configuration or utility files that directly use the secret).
- [x] T007 [US1] Modify `phase-2/src/auth/config.py` to define `JWT_SECRET_KEY` by securely reading from the `BETTER_AUTH_SECRET` environment variable, adding a fallback for development.
- [x] T008 [US1] Adjust `phase-2/src/middleware/auth.py` to correctly utilize the `JWT_SECRET_KEY` as defined in `phase-2/src/auth/config.py` for all JWT verification processes.
- [x] T009 [P] [US1] Verify that no unintended changes have affected frontend components or public variables by inspecting `phase-2/frontend/`.
- [x] T010 [US1] Run all authentication tests in `phase-2/tests/` to confirm that JWT verification functions correctly with the `BETTER_AUTH_SECRET`.

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, documentation, and cleanup.

- [x] T011 Document the change to `BETTER_AUTH_SECRET` in relevant internal documentation or READMEs (e.g., `phase-2/README.md`).
- [x] T012 Remove any lingering references or configurations for `AUTH_SECRET_KEY` from deployment environments (e.g., `.env` files, CI/CD configurations).
- [x] T013 Create a post-mortem or summary of the refactoring process, including any lessons learned, in a new markdown file (e.g., `specs/007-refactor-jwt-secret/post-mortem.md`).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User Story 1 can proceed after Foundational.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories.

### Within Each User Story

- Implementation tasks (T004-T008) are sequential.
- Verification tasks (T009-T010) depend on core implementation.

### Parallel Opportunities

- Task T009 ([P]) can potentially be done in parallel with other verification steps, if applicable, after the core changes are made.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
