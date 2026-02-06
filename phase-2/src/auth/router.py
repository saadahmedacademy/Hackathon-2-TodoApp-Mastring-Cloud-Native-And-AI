"""Authentication router with endpoints for registration, login, and token management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from .schemas import UserRegistration, UserLogin, TokenResponse, TokenRefresh
from ..services.auth_service import AuthService
from ..db.session import get_session
from ..exceptions.base import TodoValidationError

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
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
        tokens = auth_service.authenticate_user(login_data)

        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration successful but could not generate tokens"
            )

        return tokens
    except TodoValidationError as e:
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
    except Exception as e:
        # Check if this is a database integrity error (like duplicate email)
        error_msg = str(e).lower()
        if "duplicate" in error_msg or "unique" in error_msg or "constraint" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
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


@router.post("/logout")
async def logout():
    """Logout user (currently just a placeholder - in a real app would invalidate tokens)."""
    # In a real implementation, we would invalidate the refresh token
    # For now, we just return a success message
    return {"message": "Successfully logged out"}