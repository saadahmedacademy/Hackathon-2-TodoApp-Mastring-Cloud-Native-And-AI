"""Service layer for Todo business logic."""
from typing import List, Optional
from sqlmodel import Session
from ..repositories.todo_repository import TodoRepository
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..exceptions.base import TodoNotFoundException, TodoValidationError
from ..utils.validation import validate_todo_title, validate_todo_description, validate_user_id


class TodoService:
    """Service class that handles all todo-related business logic using repository pattern."""

    def __init__(self, session: Session):
        """Initialize the service with a database session."""
        self.repository = TodoRepository(session)

    def create_todo(self, user_id: str, todo_data: TodoCreate) -> Todo:
        """Create a new todo item for the specified user."""
        # Validate user_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        # Additional validation specific to Phase-II
        if not validate_todo_title(todo_data.title):
            raise TodoValidationError("Title is required and must be between 1-255 characters")

        if not validate_todo_description(todo_data.description):
            raise TodoValidationError("Description exceeds maximum length of 1000 characters")

        return self.repository.create_todo(user_id, todo_data)

    def get_all_todos(self, user_id: str, completed: Optional[bool] = None) -> List[Todo]:
        """Get all todos for the specified user, optionally filtered by completion status."""
        # Validate user_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        return self.repository.get_all_todos(user_id, completed)

    def get_todo_by_id(self, user_id: str, todo_id: int) -> Optional[Todo]:
        """Get a specific todo by ID for the specified user."""
        # Validate user_id and todo_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        if not isinstance(todo_id, int) or todo_id < 1:
            raise TodoValidationError("Invalid todo ID provided")

        return self.repository.get_todo_by_id(user_id, todo_id)

    def update_todo(self, user_id: str, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo for the specified user."""
        # Validate user_id and todo_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        if not isinstance(todo_id, int) or todo_id < 1:
            raise TodoValidationError("Invalid todo ID provided")

        # Additional validation specific to Phase-II
        if todo_data.title is not None and not validate_todo_title(todo_data.title):
            raise TodoValidationError("Title must be between 1-255 characters")

        if todo_data.description is not None and not validate_todo_description(todo_data.description):
            raise TodoValidationError("Description exceeds maximum length of 1000 characters")

        return self.repository.update_todo(user_id, todo_id, todo_data)

    def delete_todo(self, user_id: str, todo_id: int) -> bool:
        """Delete a todo by ID for the specified user."""
        # Validate user_id and todo_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        if not isinstance(todo_id, int) or todo_id < 1:
            raise TodoValidationError("Invalid todo ID provided")

        return self.repository.delete_todo(user_id, todo_id)

    def mark_complete(self, user_id: str, todo_id: int, completed: bool) -> Optional[Todo]:
        """Mark a todo as complete or incomplete for the specified user."""
        # Validate user_id and todo_id
        if not validate_user_id(user_id):
            raise TodoValidationError("Invalid user ID provided")

        if not isinstance(todo_id, int) or todo_id < 1:
            raise TodoValidationError("Invalid todo ID provided")

        if not isinstance(completed, bool):
            raise TodoValidationError("Completed status must be a boolean value")

        return self.repository.mark_complete(user_id, todo_id, completed)