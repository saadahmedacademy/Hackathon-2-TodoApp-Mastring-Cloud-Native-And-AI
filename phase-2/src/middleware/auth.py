"""Authentication middleware for global token validation."""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

from ..auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

# Load environment variables
load_dotenv()

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to handle authentication globally."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:

        # Handle preflight OPTIONS requests for CORS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Publicly accessible paths (no auth required)
        PUBLIC_PATHS = {
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
            "/health",
        }

        # Skip authentication for public paths and auth routes
        if (
            request.url.path in PUBLIC_PATHS
            or request.url.path.startswith("/auth")
        ):
            return await call_next(request)

        # Extract authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header:
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify token format (Bearer <token>)
        if not auth_header.startswith("Bearer "):
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[len("Bearer "):]

        # Verify the token
        try:
            payload = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM]
            )

            user_id: str | None = payload.get("sub")
            if user_id is None:
                from starlette.responses import JSONResponse
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Could not validate credentials"},
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Attach user info to request state
            request.state.user_id = user_id

        except JWTError:
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Could not validate credentials"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await call_next(request)
