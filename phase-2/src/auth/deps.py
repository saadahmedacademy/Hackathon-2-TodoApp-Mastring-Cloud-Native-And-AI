"""Authentication dependencies for validating JWT tokens and extracting user identity."""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

from ..auth.config import JWT_SECRET_KEY, JWT_ALGORITHM

# Load environment variables
load_dotenv()

security = HTTPBearer()


def verify_token(token: str) -> Optional[Dict]:
    """Verify and decode a JWT token, returning the payload if valid."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None


async def get_current_user(request: Request) -> str:
    """Dependency to get the current user ID from the request state (set by AuthMiddleware)."""
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return request.state.user_id