"""Authentication router with endpoints for registration, login, and token management."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from .schemas import UserRegistration, UserLogin, TokenResponse, TokenRefresh, AuthResponse, UserResponse, LogoutRequest, LogoutResponse
from ..services.auth_service import AuthService
from ..db.session import get_session
from ..exceptions.base import AppValidationError

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegistration,
    session: Session = Depends(get_session)
):
    """Register a new user and return authentication tokens."""
    try:
        auth_service = AuthService(session)
        user = auth_service.register_user(user_data)

        # After registration, also return tokens for immediate login
        login_data = UserLogin(email=user_data.email, password=user_data.password)
        auth_tokens = auth_service.authenticate_user(login_data)

        if not auth_tokens:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration successful but could not generate tokens"
            )

        # Create user response object using the Pydantic model
        user_response_obj = UserResponse(
            id=user.id,
            email=user.email,
            name=getattr(user, 'name', None),
            created_at=user.created_at.isoformat() if user.created_at else None,
            email_verified=getattr(user, 'email_verified', False)
        )

        # Return both user and token information using the AuthResponse model
        return AuthResponse(
            user=user_response_obj,
            access_token=auth_tokens.access_token,
            refresh_token=auth_tokens.refresh_token,
            token_type=auth_tokens.token_type
        )
    except AppValidationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except IntegrityError as e:
        # Handle database integrity errors like duplicate email
        error_msg = str(e).lower()
        if "duplicate" in error_msg or "unique" in error_msg or "constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        raise HTTPException(status_code=500, detail="Internal server error")
    except HTTPException:
        # Re-raise HTTPExceptions untouched
        raise
    except Exception as e:
        logging.error(f"Unhandled error during registration: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login", response_model=TokenResponse)
async def login(
    user_credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """Authenticate user and return tokens."""
    auth_service = AuthService(session)
    tokens = auth_service.authenticate_user(user_credentials)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefresh,
    session: Session = Depends(get_session)
):
    """Refresh access token using refresh token."""
    auth_service = AuthService(session)
    tokens = auth_service.refresh_access_token(token_data.refresh_token)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return tokens


@router.post("/logout", response_model=LogoutResponse)

async def logout(

    logout_data: LogoutRequest,

    session: Session = Depends(get_session)

):

    """Logout user by revoking their refresh token."""

    try:

        auth_service = AuthService(session)

        auth_service.logout_user(logout_data.refresh_token)

        return LogoutResponse(message="Successfully logged out")

    except TodoValidationError as e:

        raise HTTPException(status_code=e.status_code, detail=e.message)

    except HTTPException:

        raise

    except Exception as e:

        logging.error(f"Logout error: {e}", exc_info=True)

        raise HTTPException(status_code=500, detail="Internal server error")
