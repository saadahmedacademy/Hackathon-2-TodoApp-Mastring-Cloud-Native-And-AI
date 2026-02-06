"""Unit tests for todo viewing functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.todo_service import TodoService
from src.models.todo import Todo
from src.exceptions.base import TodoValidationError


def test_get_all_todos_success():
    """Test successful retrieval of all todos for a user."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's get_all_todos method to return dummy todos
    with patch.object(service.repository, 'get_all_todos') as mock_get_all:
        expected_todos = [
            Todo(id=1, user_id="user123", title="Todo 1", completed=False),
            Todo(id=2, user_id="user123", title="Todo 2", completed=True)
        ]

        mock_get_all.return_value = expected_todos

        # Get all todos
        user_id = "user123"
        result = service.get_all_todos(user_id)

        # Verify the result
        assert result == expected_todos
        mock_get_all.assert_called_once_with(user_id, None)


def test_get_all_todos_with_filter():
    """Test retrieval of todos with completion status filter."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    with patch.object(service.repository, 'get_all_todos') as mock_get_all:
        expected_todos = [
            Todo(id=1, user_id="user123", title="Todo 1", completed=True)
        ]

        mock_get_all.return_value = expected_todos

        # Get completed todos only
        user_id = "user123"
        result = service.get_all_todos(user_id, completed=True)

        # Verify the result
        assert result == expected_todos
        mock_get_all.assert_called_once_with(user_id, True)


def test_get_all_todos_invalid_user_id():
    """Test that getting todos with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID

    with pytest.raises(TodoValidationError):
        service.get_all_todos(user_id)


def test_get_all_todos_none_user_id():
    """Test that getting todos with None user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = None  # Invalid user ID

    with pytest.raises(TodoValidationError):
        service.get_all_todos(user_id)


def test_get_all_todos_whitespace_user_id():
    """Test that getting todos with whitespace-only user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "   "  # Invalid user ID

    with pytest.raises(TodoValidationError):
        service.get_all_todos(user_id)


if __name__ == "__main__":
    pytest.main([__file__])