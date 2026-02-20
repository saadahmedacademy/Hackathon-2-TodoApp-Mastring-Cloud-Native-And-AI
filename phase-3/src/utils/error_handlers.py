from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from typing import Any
from openai import OpenAIError, AuthenticationError, RateLimitError, APIConnectionError

# Custom Exceptions for specific application logic
class NotFoundException(HTTPException):
    def __init__(self, detail: Any = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: Any = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class InternalServerError(HTTPException):
    def __init__(self, detail: Any = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ToolExecutionException(HTTPException):
    def __init__(self, detail: Any = "Tool execution failed"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

def register_exception_handlers(app):
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": "NOT_FOUND"},
        )

    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": "BAD_REQUEST"},
        )

    @app.exception_handler(InternalServerError)
    async def internal_server_error_handler(request: Request, exc: InternalServerError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": "INTERNAL_SERVER_ERROR"},
        )

    @app.exception_handler(ToolExecutionException)
    async def tool_execution_exception_handler(request: Request, exc: ToolExecutionException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": "TOOL_EXECUTION_FAILED"},
        )

    # OpenAI API Specific Error Handlers
    @app.exception_handler(AuthenticationError)
    async def openai_authentication_error_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid OpenAI API Key provided.", "error_code": "AUTH_ERROR"},
        )

    @app.exception_handler(RateLimitError)
    async def openai_rate_limit_error_handler(request: Request, exc: RateLimitError):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "OpenAI API rate limit exceeded. Please try again later.", "error_code": "RATE_LIMIT_EXCEEDED"},
        )

    @app.exception_handler(APIConnectionError)
    async def openai_api_connection_error_handler(request: Request, exc: APIConnectionError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Could not connect to OpenAI API. Please check your network connection.", "error_code": "API_CONNECTION_ERROR"},
        )

    @app.exception_handler(OpenAIError)
    async def openai_generic_error_handler(request: Request, exc: OpenAIError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An OpenAI API error occurred: {exc.human_message}", "error_code": "OPENAI_API_ERROR"},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "error_code": "HTTP_EXCEPTION"},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Log the exception for debugging purposes in a real application
        # logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred.", "error_code": "UNEXPECTED_ERROR"},
        )
