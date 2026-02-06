"""Error handlers for the todo application."""
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .base import TodoException, TodoNotFoundException, TodoValidationError, UserMismatchException, DatabaseConnectionException


async def todo_exception_handler(request: Request, exc: TodoException):
    """Handle custom todo exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_type": "TodoException"
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_type": "HTTPException"
        }
    )


async def validation_error_handler(request: Request, exc: Exception):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": str(exc),
            "error_type": "ValidationError"
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": "GeneralException"
        }
    )


# Register these handlers in your FastAPI app
def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(TodoException, todo_exception_handler)
    app.add_exception_handler(TodoNotFoundException, todo_exception_handler)
    app.add_exception_handler(TodoValidationError, todo_exception_handler)
    app.add_exception_handler(UserMismatchException, todo_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, todo_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)  # Handle all other exceptions