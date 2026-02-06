# Quickstart Guide: Phase-II Backend

## Setup

### Prerequisites
- Python 3.11+
- pip package manager
- Access to Neon PostgreSQL database

### Installation
1. Navigate to the phase-2 directory:
   ```bash
   cd phase-2
   ```

2. Install dependencies:
   ```bash
   pip install fastapi sqlmodel uvicorn psycopg2-binary python-dotenv
   ```

3. Set up environment variables:
   ```bash
   # Create .env file with database connection details
   echo "DATABASE_URL=postgresql://username:password@host:port/database_name" > .env
   ```

## Running the Application

### Development
```bash
cd phase-2
uvicorn src.api.main:app --reload --port 8000
```

### Production
```bash
cd phase-2
uvicorn src.api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

## API Endpoints

Once running, the API will be available at `http://localhost:8000` with the following routes:
- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Update completion status

## Architecture Overview

### Models (`src/models/`)
- SQLModel classes that map to database tables
- Todo model with user_id for multi-user support

### Repositories (`src/repositories/`)
- Database access layer
- CRUD operations for Todo entities
- User-scoped queries for data isolation

### Services (`src/services/`)
- Business logic layer
- Adapter to reuse Phase-I domain logic
- Validation and error handling

### API (`src/api/`)
- FastAPI route definitions
- Request/response validation
- Error handling and serialization

## Environment Variables

- `DATABASE_URL`: Connection string for Neon PostgreSQL database
- `SECRET_KEY`: Secret key for JWT token verification (when integrated with auth)
- `DEBUG`: Enable/disable debug mode (default: false)