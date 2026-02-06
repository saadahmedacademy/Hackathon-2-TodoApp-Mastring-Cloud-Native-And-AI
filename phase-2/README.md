# Phase-II Backend: Todo API

This is the Phase-II backend implementation of the todo application, built with FastAPI and SQLModel, storing data in Neon PostgreSQL.

## Architecture

The application follows a layered architecture:

- **Models** (`src/models/`): SQLModel database models
- **Repositories** (`src/repositories/`): Database access layer
- **Services** (`src/services/`): Business logic layer with adapter to Phase-I domain logic
- **API** (`src/api/`): FastAPI route definitions

## Features

- RESTful API endpoints for todo management
- Multi-user support with data isolation via user_id
- Persistent storage in Neon PostgreSQL
- Reuse of Phase-I domain logic through adapter pattern
- Full CRUD operations for todo items

## API Endpoints

- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database connection details
   ```

3. Run the application:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```