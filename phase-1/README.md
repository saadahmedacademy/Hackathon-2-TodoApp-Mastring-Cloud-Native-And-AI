# Phase I - Console Todo Application

This folder contains all the implementation and documentation for Phase I of the console todo application.

## Overview

A simple in-memory console-based todo application built with Python, completed as Phase I of the project.

## Features

- Add new todo items with titles and optional descriptions
- View all todo items with their completion status
- Update existing todo items
- Mark todo items as complete/incomplete
- Delete todo items
- All data stored in memory during a single session

## Requirements

- Python 3.10 or higher

## Project Structure

```
.
├── src/                    # Source code
│   ├── cli/
│   │   └── main.py         # Main console application entry point
│   ├── models/
│   │   └── todo.py         # TodoItem and TodoList models
│   └── services/
│       └── todo_service.py # Business logic for todo operations
├── tests/                  # Unit tests
│   └── unit/
│       └── test_todo.py    # Unit tests for todo functionality
├── specs-todo-app/         # Specification documents
├── history/                # Prompt history records
└── demo.py                 # Demo script showing app functionality
```

## Usage

Run the application:

```bash
python src/cli/main.py
```

Or run the demo script:

```bash
python demo.py
```

## Testing

Run the unit tests:

```bash
python tests/unit/test_todo.py
```