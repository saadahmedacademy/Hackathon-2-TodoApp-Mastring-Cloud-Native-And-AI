"""Main FastAPI application for the todo backend."""
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead
from ..services.todo_service import TodoService
from ..db.session import get_session, engine
from ..exceptions.base import TodoNotFoundException, TodoValidationError
from ..utils.validation import validate_user_id, validate_todo_id
from ..exceptions.handlers import register_exception_handlers
from ..middleware.logging import add_logging_middleware
from ..auth.router import router as auth_router
from ..auth.deps import get_current_user
from ..middleware.auth import AuthMiddleware

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="REST API for managing todos with multi-user support",
    version="1.0.0"
)

# Register exception handlers
register_exception_handlers(app)

# Add logging middleware
add_logging_middleware(app)

# Add CORS middleware for frontend integration (before auth middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
        "https://hk-2-project.vercel.app/"
        ],  # Frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # Explicitly allow methods
    allow_headers=["Authorization", "Content-Type"],  # Explicitly allow headers
)


# 👇 ADD this to allow the HaggingFace as a enty point 
@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "service": "todo-backend"}


# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include authentication routes
app.include_router(auth_router)


# API Routes
@app.post("/api/tasks", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    service = TodoService(session)
    try:
        todo = service.create_todo(user_id, todo_data)
        return todo
    except TodoValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/tasks", response_model=List[TodoRead])
async def get_all_todos(
    current_user_id: str = Depends(get_current_user),
    completed: Optional[bool] = None,
    session: Session = Depends(get_session)
):
    """Retrieve all todos for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    service = TodoService(session)
    todos = service.get_all_todos(user_id, completed)
    return todos


@app.get("/api/tasks/{id}", response_model=TodoRead)
async def get_todo_by_id(
    id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Retrieve a specific todo by ID for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    # Validate todo_id format
    if not validate_todo_id(id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    service = TodoService(session)
    todo = service.get_todo_by_id(user_id, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/api/tasks/{id}", response_model=TodoRead)
async def update_todo(
    id: int,
    todo_data: TodoUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing todo for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    # Validate todo_id format
    if not validate_todo_id(id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    service = TodoService(session)
    todo = service.update_todo(user_id, id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.delete("/api/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    id: int,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific todo by ID for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    # Validate todo_id format
    if not validate_todo_id(id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    service = TodoService(session)
    success = service.delete_todo(user_id, id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")


class TodoCompleteUpdate(BaseModel):
    """Request model for updating todo completion status."""
    completed: bool


@app.patch("/api/tasks/{id}/complete", response_model=TodoRead)
async def mark_todo_complete(
    id: int,
    update_data: TodoCompleteUpdate,
    current_user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Mark a todo as complete or incomplete for the authenticated user."""
    # The user_id is now derived from the JWT token
    user_id = current_user_id

    # Validate todo_id format
    if not validate_todo_id(id):
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    service = TodoService(session)
    todo = service.mark_complete(user_id, id, update_data.completed)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "todo-api"}