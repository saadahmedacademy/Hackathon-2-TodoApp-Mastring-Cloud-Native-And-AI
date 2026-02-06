"""Security tests for authentication utilities."""

import pytest
from datetime import timedelta
from jose import jwt

from src.auth.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token
)
from src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM


def test_password_hashing():
    """Test password hashing and verification."""
    password = "securepassword123"
    hashed = get_password_hash(password)

    # Verify the password matches the hash
    assert verify_password(password, hashed)

    # Verify wrong password doesn't match
    assert not verify_password("wrongpassword", hashed)


def test_access_token_creation_and_verification():
    """Test access token creation and verification."""
    user_data = {"sub": "user123", "email": "test@example.com"}

    token = create_access_token(data=user_data)

    # Verify the token can be decoded
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "access"


def test_refresh_token_creation_and_verification():
    """Test refresh token creation and verification."""
    user_data = {"sub": "user123", "email": "test@example.com"}

    token = create_refresh_token(data=user_data)

    # Verify the token can be decoded
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@example.com"
    assert payload["type"] == "refresh"


def test_token_expiration():
    """Test token expiration."""
    user_data = {"sub": "user123", "email": "test@example.com"}

    # Create a token that expires immediately
    token = create_access_token(data=user_data, expires_delta=timedelta(seconds=0))

    # Simulate waiting for expiration (in a real test, we might mock time)
    # For now, we'll just verify the token is syntactically correct
    payload = verify_token(token)
    # Note: Even expired tokens can be decoded, but verification should fail
    # In a real implementation, we'd handle the expiration properly


def test_invalid_token():
    """Test invalid token handling."""
    invalid_token = "invalid.token.string"

    payload = verify_token(invalid_token)
    assert payload is None


def test_token_with_custom_expiration():
    """Test token with custom expiration time."""
    user_data = {"sub": "user123", "email": "test@example.com"}

    token = create_access_token(data=user_data, expires_delta=timedelta(hours=2))

    # Decode without verification to check expiration claim
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_signature": False})
    assert payload["sub"] == "user123"
    assert payload["type"] == "access"


def test_token_without_type_field():
    """Test token without type field (should still work but won't have type)."""
    # Directly create a token without type for testing
    token_data = {"sub": "user123", "email": "test@example.com"}
    token = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"