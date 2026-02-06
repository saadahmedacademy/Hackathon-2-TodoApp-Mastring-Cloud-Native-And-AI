"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegistration(BaseModel):
    """Schema for user registration requests."""

    email: EmailStr
    password: str
    name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login requests."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token responses."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh requests."""

    refresh_token: str


class UserResponse(BaseModel):
    """Schema for user information responses."""

    id: str
    email: str
    name: Optional[str] = None
    created_at: str
    email_verified: bool = False