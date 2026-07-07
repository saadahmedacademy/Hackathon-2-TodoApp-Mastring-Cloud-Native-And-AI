"""Authentication dependencies for validating JWT tokens and extracting user identity."""

from fastapi import HTTPException, status, Request
from typing import Dict, Optional


async def get_current_user(request: Request) -> str:
    """Dependency to get the current user ID from the request state (set by AuthMiddleware)."""
    if (
        not hasattr(request.state, 'user_id') 
        or request.state.user_id is None
        or not isinstance(request.state.user_id, str)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return request.state.user_id
