# Console Todo Application

A simple in-memory console-based todo application built with Python.

## Features

- Add new todo items with titles and optional descriptions
- View all todo items with their completion status
- Update existing todo items
- Mark todo items as complete
- Delete todo items
- All data stored in memory during a single session

## Requirements

- Python 3.10 or higher

## Installation

1. Clone or download this repository
2. Navigate to the project directory

## Usage

Run the application:

```bash
python src/cli/main.py
```

Follow the on-screen menu to interact with the application:

1. Add Todo - Create new todo items
2. View Todos - See all your todo items
3. Update Todo - Modify existing todo items
4. Mark Complete - Mark items as completed
5. Delete Todo - Remove items from your list
6. Exit - Quit the application

## Project Structure

```
src/
├── models/
│   └── todo.py                 # TodoItem and TodoList models
├── services/
│   └── todo_service.py         # Business logic for todo operations
└── cli/
    └── main.py                 # Main console application entry point

tests/
└── unit/
    └── test_todo.py            # Unit tests for todo functionality
```

## Testing

Run the unit tests:

```bash
python tests/unit/test_todo.py
```

## Architecture

The application follows a clean architecture pattern:

- **Models**: Handle data structures and validation
- **Services**: Contain business logic and operations
- **CLI**: Handles user interface and input/output