# Feature Specification: Phase-II Backend Core

**Feature Branch**: `002-backend-core`
**Created**: 2026-02-02
**Status**: Draft
**Input**: Building upon the Console Todo Application spec from `/specs/001-console-todo-app/spec.md`

## Overview

This specification describes the Phase-II Backend Core, which transforms the console-based todo application into a web-based REST API using FastAPI and SQLModel. The backend will persist data in Neon PostgreSQL while reusing the Phase-I domain logic through an adapter pattern.

## User Scenarios & Testing *(mandatory)*

Based on the original console application requirements, adapted for web API consumption:

### User Story 1 - Add New Todo Item via API (Priority: P1)

As a client application, I want to add a new todo item via REST API so that I can persist tasks for a specific user.

**Independent Test**: Can be fully tested by making a POST request to create a todo with a title and optional description, and verifying the item is created in the database with a unique ID and incomplete status.

**Acceptance Scenarios**:
1. **Given** I make a POST request to `/api/{user_id}/tasks` with valid title, **When** I submit the request, **Then** a new todo item is created with a unique ID, the provided title, an optional description (if provided), and an incomplete status.
2. **Given** I make a POST request to `/api/{user_id}/tasks` without a title, **When** I submit the request, **Then** I receive a 400 error response with an appropriate error message.

---

### User Story 2 - View All Todo Items via API (Priority: P1)

As a client application, I want to view all todo items for a user via REST API so that I can display the user's tasks and their completion status.

**Independent Test**: Can be fully tested by creating some todos and then making a GET request to view the complete list to verify all items display correctly with their ID, title, and completion status.

**Acceptance Scenarios**:
1. **Given** I have added one or more todo items for a user, **When** I make a GET request to `/api/{user_id}/tasks`, **Then** I see a list displaying each item's ID, title, and completion status.
2. **Given** I have no todo items for a user, **When** I make a GET request to `/api/{user_id}/tasks`, **Then** I see an empty array response.

---

### User Story 3 - Mark Todo as Complete via API (Priority: P2)

As a client application, I want to mark a todo item as complete via REST API so that I can track which tasks a user has finished.

**Independent Test**: Can be fully tested by creating a todo, making a PATCH request to mark it as complete using its ID, and verifying the status updates correctly.

**Acceptance Scenarios**:
1. **Given** I have an incomplete todo item, **When** I make a PATCH request to `/api/{user_id}/tasks/{id}/complete` with `completed: true`, **Then** the item's status changes to completed.
2. **Given** I attempt to mark a non-existent todo as complete, **When** I make a request with an invalid ID, **Then** I receive a 404 error response.

---

### User Story 4 - Update Todo Details via API (Priority: P2)

As a client application, I want to update the details of an existing todo via REST API so that users can modify titles or descriptions as needed.

**Independent Test**: Can be fully tested by creating a todo, making a PUT request to update its details using its ID, and verifying the changes persist.

**Acceptance Scenarios**:
1. **Given** I have an existing todo item, **When** I make a PUT request to `/api/{user_id}/tasks/{id}` with new details, **Then** the item's information is updated accordingly.
2. **Given** I attempt to update a non-existent todo, **When** I make a request with an invalid ID, **Then** I receive a 404 error response.

---

### User Story 5 - Delete Todo Item via API (Priority: P3)

As a client application, I want to delete a todo item via REST API so that users can remove tasks they no longer need to track.

**Independent Test**: Can be fully tested by creating a todo, making a DELETE request to remove it using its ID, and verifying it no longer appears in the list.

**Acceptance Scenarios**:
1. **Given** I have an existing todo item, **When** I make a DELETE request to `/api/{user_id}/tasks/{id}`, **Then** the item is removed from the database with a 204 response.
2. **Given** I attempt to delete a non-existent todo, **When** I make a request with an invalid ID, **Then** I receive a 404 error response.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a REST API with endpoints for all todo operations
- **FR-002**: System MUST persist todo data in Neon PostgreSQL database
- **FR-003**: System MUST enforce user ownership of todos through user_id
- **FR-004**: System MUST reuse Phase-I domain logic via an adapter pattern
- **FR-005**: System MUST handle all error conditions gracefully with appropriate HTTP status codes
- **FR-006**: System MUST provide clear API responses with appropriate success/error messages
- **FR-007**: System MUST assign unique IDs to each todo item automatically
- **FR-008**: System MUST handle attempts to update, complete, or delete non-existent todos appropriately

### Key Entities *(include if feature involves data)*

- **Todo Item**: Represents a single task with attributes: unique ID (integer), user_id (string), title (string, required), description (string, optional), completion status (boolean, default: false), created_at, updated_at
- **User**: Represents a user with unique user_id (string) for data isolation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Client applications can successfully add, view, update, mark complete, and delete todo items via API calls
- **SC-002**: Data persists in Neon PostgreSQL database across application restarts
- **SC-003**: All five core operations (add, view, update, complete, delete) are accessible via well-defined REST endpoints
- **SC-004**: API handles all error scenarios gracefully with appropriate HTTP status codes
- **SC-005**: Codebase demonstrates clean separation of concerns with models, repositories, services, and API layers
- **SC-006**: All functionality is accessible through well-documented REST API endpoints