# CLI Contract: Console Todo Application

## Overview
The console todo application provides a command-line interface for managing todo items. The application presents a menu-driven interface where users can select operations to perform on their todo list.

## Core Operations

### 1. Add Todo Item
**Command**: Menu selection "Add Todo" or option 1
**Input**:
- title (string, required)
- description (string, optional)
**Output**: Confirmation message with assigned ID
**Error Conditions**:
- Empty title returns error message
- Invalid input returns error message

### 2. View All Todo Items
**Command**: Menu selection "View Todos" or option 2
**Input**: None
**Output**: List of all todo items with ID, title, and completion status
**Error Conditions**: None (empty list is valid)

### 3. Update Todo Item
**Command**: Menu selection "Update Todo" or option 3
**Input**:
- todo_id (integer, required)
- new_title (string, optional)
- new_description (string, optional)
**Output**: Confirmation message of update
**Error Conditions**:
- Invalid ID returns error
- Non-existent ID returns error

### 4. Mark Todo as Complete
**Command**: Menu selection "Mark Complete" or option 4
**Input**:
- todo_id (integer, required)
**Output**: Confirmation message of completion status change
**Error Conditions**:
- Invalid ID returns error
- Non-existent ID returns error

### 5. Delete Todo Item
**Command**: Menu selection "Delete Todo" or option 5
**Input**:
- todo_id (integer, required)
**Output**: Confirmation message of deletion
**Error Conditions**:
- Invalid ID returns error
- Non-existent ID returns error

### 6. Exit Application
**Command**: Menu selection "Exit" or option 6
**Input**: None
**Output**: Goodbye message and application termination
**Error Conditions**: None

## Data Types
- **todo_id**: Positive integer (auto-incremented)
- **title**: Non-empty string (required for creation)
- **description**: String (optional, can be empty/null)
- **completed**: Boolean (default: False)

## Error Responses
All error conditions return user-friendly error messages that explain what went wrong and how to correct the issue.

## Success Responses
All successful operations return confirmation messages that indicate what action was taken and its result.