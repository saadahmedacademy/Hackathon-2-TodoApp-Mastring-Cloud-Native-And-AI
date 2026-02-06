"""Base exception classes for the todo application."""


class TodoException(Exception):
    """Base exception for todo-related errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TodoNotFoundException(TodoException):
    """Raised when a todo item is not found."""

    def __init__(self, todo_id: int):
        super().__init__(
            message=f"Todo with ID {todo_id} not found",
            status_code=404
        )


class TodoValidationError(TodoException):
    """Raised when validation fails for todo operations."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422  # Unprocessable Entity
        )


class UserMismatchException(TodoException):
    """Raised when a user tries to access another user's todo."""

    def __init__(self, user_id: str, todo_id: int):
        super().__init__(
            message=f"User {user_id} does not have permission to access todo with ID {todo_id}",
            status_code=403  # Forbidden
        )


class DatabaseConnectionException(TodoException):
    """Raised when there are issues connecting to the database."""

    def __init__(self, message: str = "Database connection error"):
        super().__init__(
            message=message,
            status_code=500
        )