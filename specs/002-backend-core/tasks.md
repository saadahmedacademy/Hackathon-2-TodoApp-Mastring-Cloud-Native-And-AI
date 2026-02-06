# Tasks: Phase-II Backend Todo Application

**Feature**: Console Todo Application → Web Backend | **Date**: 2026-02-02 | **Spec**: spec.md
**Plan**: plan.md | **Branch**: `002-backend-core`

## Overview

This document breaks down the implementation of the Phase-II backend for the todo application. The goal is to create a FastAPI backend that exposes task management APIs, persists data in Neon PostgreSQL, and reuses Phase-I domain logic via an adapter layer.

### User Story Priorities

- **P1**: Critical functionality that forms the core of the application
- **P2**: Important features that enhance the core functionality
- **P3**: Nice-to-have features that complete the experience

### Implementation Strategy

1. **MVP Scope**: Implement User Story 1 (Add New Todo) and User Story 2 (View All Todos) first to create a minimal viable product
2. **Incremental Delivery**: Add features in priority order (P1 → P2 → P3)
3. **Test-Driven Approach**: Each user story includes its own tests to ensure independent verification
4. **Parallel Opportunities**: Identified with [P] markers for efficient execution

## Dependencies

- User Story 2 (View) can be developed independently of User Story 1 (Add)
- User Story 3 (Mark Complete) depends on User Story 1 (Add) being implemented first
- User Story 4 (Update) depends on User Story 1 (Add) being implemented first
- User Story 5 (Delete) depends on User Story 1 (Add) being implemented first

## Parallel Execution Examples

- **User Story 1**: Models and Repository tasks can run in parallel [P]
- **User Story 2**: Service and API tasks can run in parallel [P]
- **User Story 3**: Implementation can run in parallel with User Story 4 after User Story 1 completion

---

## Phase 1: Setup Tasks

Goal: Initialize project structure and install dependencies

- [X] T001 Create phase-2 directory structure per implementation plan
- [X] T002 Set up requirements.txt with FastAPI, SQLModel, and testing dependencies
- [X] T003 Initialize src/models, src/services, src/repositories, and src/api directories
- [X] T004 Set up basic configuration files (.env.example, .gitignore)
- [X] T005 Create basic project documentation (README.md)

---

## Phase 2: Foundational Tasks

Goal: Establish core architecture patterns and reusable components

- [X] T010 [P] Implement database session management in src/db/session.py
- [X] T011 [P] Set up database engine and connection in src/db/engine.py
- [X] T012 Create adapter pattern to reuse Phase-I domain logic in src/services/adapter.py
- [X] T013 Implement base exception classes in src/exceptions/base.py
- [X] T014 Set up logging configuration in src/utils/logging.py
- [X] T015 Create utility functions for input validation in src/utils/validation.py

---

## Phase 3: User Story 1 - Add New Todo Item (Priority: P1)

Goal: As a user, I want to add a new todo item to my list so that I can keep track of tasks I need to complete during my current session.

**Independent Test**: Can be fully tested by sending POST request to create a todo with a title and optional description, and verifying the item is created in the database with a unique ID and incomplete status.

- [X] T020 [P] [US1] Create Todo model with SQLModel in src/models/todo.py
- [X] T021 [P] [US1] Create TodoCreate schema in src/models/todo.py
- [X] T022 [P] [US1] Create TodoRead schema in src/models/todo.py
- [X] T023 [US1] Implement TodoRepository.create_todo method in src/repositories/todo_repository.py
- [X] T024 [US1] Implement TodoService.create_todo method in src/services/todo_service.py
- [X] T025 [US1] Create POST /api/{user_id}/tasks endpoint in src/api/main.py
- [X] T026 [US1] Add input validation for title and description in src/api/main.py
- [X] T027 [US1] Test User Story 1 functionality with unit tests in tests/unit/test_todo_creation.py
- [X] T028 [US1] Test User Story 1 functionality with integration tests in tests/integration/test_todo_creation.py

---

## Phase 4: User Story 2 - View All Todo Items (Priority: P1)

Goal: As a user, I want to view all my todo items so that I can see what tasks I have to do and their completion status.

**Independent Test**: Can be fully tested by adding some todos and then sending GET request to view the complete list to verify all items display correctly with their ID, title, and completion status.

- [X] T030 [P] [US2] Create TodoUpdate schema in src/models/todo.py
- [X] T031 [US2] Implement TodoRepository.get_all_todos method in src/repositories/todo_repository.py
- [X] T032 [US2] Implement TodoService.get_all_todos method in src/services/todo_service.py
- [X] T033 [US2] Create GET /api/{user_id}/tasks endpoint in src/api/main.py
- [X] T034 [US2] Add filtering capability for completed status in src/api/main.py
- [X] T035 [US2] Test User Story 2 functionality with unit tests in tests/unit/test_todo_view.py
- [X] T036 [US2] Test User Story 2 functionality with integration tests in tests/integration/test_todo_view.py

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P2)

Goal: As a user, I want to mark a todo item as complete so that I can track which tasks I have finished.

**Independent Test**: Can be fully tested by adding a todo, sending PATCH request to mark it as complete using its ID, and verifying the status updates correctly.

- [X] T040 [P] [US3] Add mark_complete method to TodoRepository in src/repositories/todo_repository.py
- [X] T041 [US3] Implement TodoService.mark_complete method in src/services/todo_service.py
- [X] T042 [US3] Create PATCH /api/{user_id}/tasks/{id}/complete endpoint in src/api/main.py
- [X] T043 [US3] Add validation for todo existence in src/api/main.py
- [X] T044 [US3] Test User Story 3 functionality with unit tests in tests/unit/test_todo_completion.py
- [X] T045 [US3] Test User Story 3 functionality with integration tests in tests/integration/test_todo_completion.py

---

## Phase 6: User Story 4 - Update Todo Details (Priority: P2)

Goal: As a user, I want to update the details of an existing todo so that I can modify titles or descriptions as needed.

**Independent Test**: Can be fully tested by adding a todo, sending PUT request to update its details using its ID, and verifying the changes persist.

- [X] T050 [P] [US4] Add update_todo method to TodoRepository in src/repositories/todo_repository.py
- [X] T051 [US4] Implement TodoService.update_todo method in src/services/todo_service.py
- [X] T052 [US4] Create PUT /api/{user_id}/tasks/{id} endpoint in src/api/main.py
- [X] T053 [US4] Add validation for update operations in src/api/main.py
- [X] T054 [US4] Test User Story 4 functionality with unit tests in tests/unit/test_todo_update.py
- [X] T055 [US4] Test User Story 4 functionality with integration tests in tests/integration/test_todo_update.py

---

## Phase 7: User Story 5 - Delete Todo Item (Priority: P3)

Goal: As a user, I want to delete a todo item so that I can remove tasks I no longer need to track.

**Independent Test**: Can be fully tested by adding a todo, sending DELETE request to remove it using its ID, and verifying it no longer appears in the list.

- [X] T060 [P] [US5] Add delete_todo method to TodoRepository in src/repositories/todo_repository.py
- [X] T061 [US5] Implement TodoService.delete_todo method in src/services/todo_service.py
- [X] T062 [US5] Create DELETE /api/{user_id}/tasks/{id} endpoint in src/api/main.py
- [X] T063 [US5] Add validation for delete operations in src/api/main.py
- [X] T064 [US5] Test User Story 5 functionality with unit tests in tests/unit/test_todo_delete.py
- [X] T065 [US5] Test User Story 5 functionality with integration tests in tests/integration/test_todo_delete.py

---

## Phase 8: User Story 6 - Get Single Todo (Additional Enhancement)

Goal: As a user, I want to retrieve a specific todo item so that I can see detailed information about a particular task.

**Independent Test**: Can be fully tested by adding a todo and then sending GET request to retrieve it by its ID, verifying it returns the correct details.

- [X] T070 [P] [US6] Add get_todo_by_id method to TodoRepository in src/repositories/todo_repository.py
- [X] T071 [US6] Implement TodoService.get_todo_by_id method in src/services/todo_service.py
- [X] T072 [US6] Create GET /api/{user_id}/tasks/{id} endpoint in src/api/main.py
- [X] T073 [US6] Test User Story 6 functionality with unit tests in tests/unit/test_todo_retrieval.py
- [X] T074 [US6] Test User Story 6 functionality with integration tests in tests/integration/test_todo_retrieval.py

---

## Phase 9: Polish & Cross-Cutting Concerns

Goal: Complete the implementation with error handling, documentation, and deployment readiness

- [X] T080 Implement comprehensive error handling in src/exceptions/handlers.py
- [X] T081 Add request/response logging middleware in src/middleware/logging.py
- [X] T082 Create API documentation with Swagger/OpenAPI in src/api/main.py
- [X] T083 Implement proper database migration system with Alembic
- [X] T084 Add authentication middleware placeholder in src/middleware/auth.py
- [X] T085 Create comprehensive integration tests in tests/integration/test_full_workflow.py
- [X] T086 Update README.md with API documentation and usage examples
- [X] T087 Set up environment configuration for different environments (dev, prod)
- [X] T088 Perform final integration testing and bug fixes
- [X] T089 Prepare deployment documentation in docs/deployment.md