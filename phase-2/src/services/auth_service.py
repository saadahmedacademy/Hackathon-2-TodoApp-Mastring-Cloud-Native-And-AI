"""Authentication service for user registration, login, and token management."""

from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
import uuid
import logging

from ..models.user import User
from ..auth.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from ..auth.schemas import UserRegistration, UserLogin, TokenResponse
from ..exceptions.base import TodoValidationError


class AuthService:
    """Service class for handling authentication operations."""

    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_data: UserRegistration) -> User:
        """Register a new user with the provided data."""
        # Check if user already exists
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise TodoValidationError("This email is already in use. Please use a different email or sign in.", status_code=409)

        # Validate password strength (basic validation)
        if len(user_data.password) < 8:
            raise TodoValidationError("Password must be at least 8 characters long", status_code=400)

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            id=str(uuid.uuid4()),
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name
        )

        self.session.add(user)
        try:
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
            # Check if this is a database integrity error (like duplicate email)
            error_str = str(e).lower()
            if "duplicate" in error_str or "unique" in error_str or "constraint" in error_str:
                self.session.rollback()
                raise TodoValidationError("This email is already in use. Please use a different email or sign in.", status_code=409)

            self.session.rollback()
            logging.error(f"Error during user registration and commit: {e}", exc_info=True)
            raise TodoValidationError(f"Registration failed: {str(e)}", status_code=500)

    def authenticate_user(self, user_login: UserLogin) -> Optional[TokenResponse]:
        """Authenticate user credentials and return tokens if valid."""
        # Find user by email
        user = self.session.exec(
            select(User).where(User.email == user_login.email)
        ).first()

        if not user or not verify_password(user_login.password, user.password_hash):
            return None

        # Create access and refresh tokens
        user_data = {"sub": user.id, "email": user.email}

        access_token = create_access_token(
            data=user_data,
            expires_delta=timedelta(minutes=15)  # Using default 15 min for access token
        )

        refresh_token = create_refresh_token(
            data=user_data
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """Refresh access token using the provided refresh token."""
        # In a real implementation, we'd validate the refresh token against a stored token
        # For now, we'll decode and verify the token to extract user info
        from ..auth.security import verify_token

        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        # Verify user still exists
        user = self.session.get(User, user_id)
        if not user:
            return None

        # Create new access token
        user_data = {"sub": user.id, "email": user.email}
        new_access_token = create_access_token(data=user_data)
        new_refresh_token = create_refresh_token(data=user_data)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )