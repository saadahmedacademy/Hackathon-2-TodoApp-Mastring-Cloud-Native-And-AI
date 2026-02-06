---
description: "Task list for Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below adjusted for console todo application structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure in src/
- [ ] T002 [P] Create src/models/ directory
- [ ] T003 [P] Create src/services/ directory
- [ ] T004 [P] Create src/cli/ directory
- [ ] T005 [P] Create tests/unit/ directory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create TodoItem model in src/models/todo.py
- [ ] T007 Create TodoList collection model in src/models/todo.py
- [ ] T008 Create TodoService class in src/services/todo_service.py
- [ ] T009 Implement basic CLI framework in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo Item (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items with unique ID, title, and optional description

**Independent Test**: Can be fully tested by running the application, selecting the add option, entering a title and optional description, and verifying the item appears in the list with a unique ID and incomplete status.

### Implementation for User Story 1

- [x] T010 [US1] Implement add_todo method in src/services/todo_service.py
- [x] T011 [US1] Add validation for required title in src/services/todo_service.py
- [x] T012 [US1] Implement CLI interface for adding todo in src/cli/main.py
- [x] T013 [US1] Connect add todo functionality to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Todo Items (Priority: P1)

**Goal**: Allow users to view all their todo items with ID, title, and completion status

**Independent Test**: Can be fully tested by adding some todos and then viewing the complete list to verify all items display correctly with their ID, title, and completion status.

### Implementation for User Story 2

- [x] T014 [US2] Implement get_all_todos method in src/services/todo_service.py
- [x] T015 [US2] Implement CLI interface for viewing todos in src/cli/main.py
- [x] T016 [US2] Connect view todos functionality to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P2)

**Goal**: Allow users to mark a todo item as complete using its ID

**Independent Test**: Can be fully tested by adding a todo, marking it as complete using its ID, and verifying the status updates correctly.

### Implementation for User Story 3

- [x] T017 [US3] Implement mark_complete method in src/services/todo_service.py
- [x] T018 [US3] Add validation for existing todo ID in src/services/todo_service.py
- [x] T019 [US3] Implement CLI interface for marking complete in src/cli/main.py
- [x] T020 [US3] Connect mark complete functionality to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Todo Details (Priority: P2)

**Goal**: Allow users to update the details of an existing todo using its ID

**Independent Test**: Can be fully tested by adding a todo, updating its details using its ID, and verifying the changes persist.

### Implementation for User Story 4

- [x] T021 [US4] Implement update_todo method in src/services/todo_service.py
- [x] T022 [US4] Add validation for existing todo ID in src/services/todo_service.py
- [x] T023 [US4] Implement CLI interface for updating todo in src/cli/main.py
- [x] T024 [US4] Connect update todo functionality to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Delete Todo Item (Priority: P3)

**Goal**: Allow users to delete a todo item using its ID

**Independent Test**: Can be fully tested by adding a todo, deleting it using its ID, and verifying it no longer appears in the list.

### Implementation for User Story 5

- [x] T025 [US5] Implement delete_todo method in src/services/todo_service.py
- [x] T026 [US5] Add validation for existing todo ID in src/services/todo_service.py
- [x] T027 [US5] Implement CLI interface for deleting todo in src/cli/main.py
- [x] T028 [US5] Connect delete todo functionality to CLI menu in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T029 [P] Add comprehensive error handling in src/services/todo_service.py
- [x] T030 [P] Add user-friendly error messages in src/cli/main.py
- [x] T031 [P] Add input validation across all CLI operations in src/cli/main.py
- [x] T032 [P] Add docstrings to all public methods in src/models/todo.py and src/services/todo_service.py
- [x] T033 Implement graceful exit functionality in src/cli/main.py
- [x] T034 Run quickstart.md validation

---
## Phase 9: User Story 6 - Mark Todo as Incomplete (Priority: P2)
**Goal**: Allow users to mark a todo item as incomplete using its ID

**Independent Test**: Can be fully tested by adding a todo, marking it as complete, then marking it as incomplete using its ID, and verifying the status updates correctly.

### Implementation for User Story 6

- [x] T035 [US6] Implement mark_incomplete method in src/services/todo_service.py
- [x] T036 [US6] Implement CLI interface for marking incomplete in src/cli/main.py
- [x] T037 [US6] Connect mark incomplete functionality to CLI menu in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 3, 4, 5 AND 6 should all work independently

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P6)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Implement add_todo method in src/services/todo_service.py"
Task: "Implement CLI interface for adding todo in src/cli/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence