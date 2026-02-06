"""Request/response logging middleware for the todo application."""
import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.logging import log_info, log_error


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next):
        """Process the request and log details."""
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        # Log request details
        start_time = time.time()
        log_info(
            "Request received",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "headers": dict(request.headers),
                "client": request.client.host if request.client else None
            }
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response details
            log_info(
                "Response sent",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "duration_ms": round(duration * 1000, 2),
                    "content_length": response.headers.get("content-length", "unknown")
                }
            )

            return response
        except Exception as e:
            # Calculate duration for error case
            duration = time.time() - start_time

            # Log error details
            log_error(
                "Request failed with exception",
                extra={
                    "request_id": request_id,
                    "exception": str(e),
                    "duration_ms": round(duration * 1000, 2)
                }
            )

            # Re-raise the exception to be handled by the exception handlers
            raise


def add_logging_middleware(app):
    """Add logging middleware to the FastAPI app."""
    app.add_middleware(LoggingMiddleware)