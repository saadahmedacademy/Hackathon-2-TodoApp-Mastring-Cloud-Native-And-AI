"""Utility functions for input validation in the todo application."""
import re
from typing import Optional


def validate_todo_title(title: str) -> bool:
    """
    Validate a todo title.

    Args:
        title: The title to validate

    Returns:
        True if valid, False otherwise
    """
    if not title or not isinstance(title, str):
        return False

    # Check if title is empty after stripping whitespace
    if not title.strip():
        return False

    # Check length constraints (1-255 characters as per data model)
    if len(title) < 1 or len(title) > 255:
        return False

    return True


def validate_todo_description(description: Optional[str]) -> bool:
    """
    Validate a todo description.

    Args:
        description: The description to validate (can be None)

    Returns:
        True if valid, False otherwise
    """
    if description is None:
        return True  # Description is optional

    if not isinstance(description, str):
        return False

    # Check length constraints (max 1000 characters as per data model)
    if len(description) > 1000:
        return False

    return True


def validate_user_id(user_id: str) -> bool:
    """
    Validate a user ID.

    Args:
        user_id: The user ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id or not isinstance(user_id, str):
        return False

    # Check if user_id is empty after stripping whitespace
    if not user_id.strip():
        return False

    # Basic check: alphanumeric, underscores, hyphens, dots, and length constraints
    if len(user_id) < 1 or len(user_id) > 100:
        return False

    # Check for valid characters (alphanumeric, underscore, hyphen, dot)
    if not re.match(r'^[a-zA-Z0-9._-]+$', user_id):
        return False

    return True


def sanitize_input(text: str) -> str:
    """
    Sanitize input text by removing potentially dangerous characters.

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove null bytes and other potentially dangerous characters
    sanitized = text.replace('\0', '')

    # Strip leading/trailing whitespace
    return sanitized.strip()


def validate_todo_id(todo_id: int) -> bool:
    """
    Validate a todo ID.

    Args:
        todo_id: The todo ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(todo_id, int):
        return False

    # Todo IDs should be positive integers
    if todo_id < 1:
        return False

    return True