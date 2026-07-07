"""Authentication middleware for global token validation."""

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from ..auth.security import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authentication globally."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:

        if request.method == "OPTIONS":
            return await call_next(request)

        PUBLIC_PATHS = {
            "/",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
            "/health",
        }

        if request.url.path == "/" and "logs=container" in request.url.query:
            return await call_next(request)

        if (
            request.url.path in PUBLIC_PATHS
            or request.url.path.startswith("/auth")
        ):
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[len("Bearer "):]

        payload = verify_token(token)
        if not payload or payload.get("sub") is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        request.state.user_id = payload.get("sub")
        return await call_next(request)
