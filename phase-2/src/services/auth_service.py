"""Authentication service for user registration, login, and token management."""

from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta, datetime
import uuid
import logging

from ..models.user import User
from ..models.revoked_token import RevokedToken                          
from ..auth.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token                                                         
)
from ..auth.schemas import UserRegistration, UserLogin, TokenResponse
from ..exceptions.base import TodoValidationError


class AuthService:
    """Service class for handling authentication operations."""

    def __init__(self, session: Session):
        self.session = session

    def register_user(self, user_data: UserRegistration) -> User:
        """Register a new user with the provided data."""
        existing_user = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()

        if existing_user:
            raise TodoValidationError("Email already registered", status_code=409)

        if len(user_data.password) < 8:
            raise TodoValidationError(
                "Password must be at least 8 characters long",
                status_code=400
            )

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
            error_str = str(e).lower()
            if "duplicate" in error_str or "unique" in error_str or "constraint" in error_str:
                self.session.rollback()
                raise TodoValidationError("Email already registered", status_code=409)

            self.session.rollback()
            logging.error(f"Error during user registration: {e}", exc_info=True)
            raise TodoValidationError(f"Registration failed: {str(e)}", status_code=500)

    def authenticate_user(self, user_login: UserLogin) -> Optional[TokenResponse]:
        """Authenticate user credentials and return tokens if valid."""
        user = self.session.exec(
            select(User).where(User.email == user_login.email)
        ).first()

        if not user or not verify_password(user_login.password, user.password_hash):
            return None

        user_data = {"sub": user.id, "email": user.email}

        access_token = create_access_token(
            data=user_data,
            expires_delta=timedelta(minutes=15)
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
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # ✅ Bug 2 fix — correct indentation, jti check is self-contained
        jti = payload.get("jti")
        if jti:
            revoked = self.session.exec(
                select(RevokedToken).where(RevokedToken.token_jti == jti)
            ).first()
            if revoked:
                return None  # token is on the banned list

        # ✅ Bug 2 fix — happy path now actually returns new tokens
        user_id = payload.get("sub")
        email = payload.get("email")
        if not user_id:
            return None

        user_data = {"sub": user_id, "email": email}
        access_token = create_access_token(
            data=user_data,
            expires_delta=timedelta(minutes=15)
        )
        new_refresh_token = create_refresh_token(data=user_data)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    def logout_user(self, refresh_token: str) -> bool:
        """Revoke a refresh token so it can never be used again."""
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise TodoValidationError("Invalid refresh token", status_code=401)

        jti = payload.get("jti")
        exp = payload.get("exp")
        if not jti:
            raise TodoValidationError("Token has no jti claim", status_code=400)

        # Idempotent — if already revoked, that's fine
        existing = self.session.exec(
            select(RevokedToken).where(RevokedToken.token_jti == jti)
        ).first()
        if existing:
            return True

        revoked = RevokedToken(
            token_jti=jti,
            expires_at=datetime.utcfromtimestamp(exp)
        )
        self.session.add(revoked)
        self.session.commit()
        return True
