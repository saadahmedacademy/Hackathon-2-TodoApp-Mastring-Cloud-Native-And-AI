---
id: 1
title: add-mark-incomplete-functionality
stage: impl
date: '2026-02-01'
surface: agent
model: claude-sonnet-4-5-20250929
feature: console-todo-app
branch: 001-console-todo-app
user: saadahmed
command: sp.implement
labels:
  - todo
  - cli
  - functionality
  - enhancement
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/models/todo.py
  - src/services/todo_service.py
  - src/cli/main.py
  - specs/001-console-todo-app/data-model.md
  - specs/001-console-todo-app/tasks.md
tests:
  - test_mark_incomplete.py
---

# Add Mark Incomplete Functionality

## Summary
Implemented the ability to mark todo items as incomplete in the console todo application. This extends the existing functionality that only allowed marking items as complete.

## Changes Made

### 1. Updated Data Model
- Modified the data model documentation to reflect that todos can transition both to complete and back to incomplete states

### 2. Enhanced Models Layer
- Added `mark_incomplete` method to the `TodoList` class in `src/models/todo.py`
- Method allows setting the `completed` status back to `False`

### 3. Enhanced Services Layer
- Added `mark_incomplete` method to the `TodoService` class in `src/services/todo_service.py`
- Method delegates to the underlying `TodoList` instance

### 4. Enhanced CLI Interface
- Added `mark_incomplete` function in `src/cli/main.py` to handle user input
- Updated the menu display to include "Mark Incomplete" option (option 5)
- Updated the main loop to handle the new menu option
- Adjusted menu numbering: Delete moved from 5 to 6, Exit moved from 6 to 7
- Updated user input validation to accept choices 1-7

### 5. Updated Task Documentation
- Added User Story 6 for the mark incomplete functionality
- Updated task dependencies and incremental delivery sections

## Testing
Created a comprehensive test (`test_mark_incomplete.py`) that verifies:
- Adding a new todo creates it as incomplete
- Marking complete works as before
- Marking incomplete works correctly
- Invalid IDs return False appropriately

## Outcome
The application now supports bidirectional state transitions for todo items:
- New todos start as incomplete
- Users can mark todos as complete
- Users can now also mark todos as incomplete
- Menu system has been updated to include this new functionality

## Evaluation
The implementation follows the existing code patterns and maintains consistency with the established architecture. All changes are backward compatible and extend the existing functionality without breaking any existing features.