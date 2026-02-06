"""Unit tests for todo retrieval functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.todo_service import TodoService
from src.models.todo import Todo
from src.exceptions.base import TodoValidationError


def test_get_todo_by_id_success():
    """Test successful retrieval of a todo by ID."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's get_todo_by_id method to return a dummy todo
    with patch.object(service.repository, 'get_todo_by_id') as mock_get_by_id:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Retrieved Todo"
        expected_todo.description = "Retrieved Description"
        expected_todo.completed = False
        expected_todo.user_id = "user123"

        mock_get_by_id.return_value = expected_todo

        # Get a todo by ID
        user_id = "user123"
        todo_id = 1

        result = service.get_todo_by_id(user_id, todo_id)

        # Verify the result
        assert result == expected_todo
        mock_get_by_id.assert_called_once_with(user_id, todo_id)


def test_get_nonexistent_todo_by_id():
    """Test retrieval of a nonexistent todo by ID."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    with patch.object(service.repository, 'get_todo_by_id') as mock_get_by_id:
        mock_get_by_id.return_value = None  # Todo not found

        # Get a nonexistent todo by ID
        user_id = "user123"
        todo_id = 9999

        result = service.get_todo_by_id(user_id, todo_id)

        # Verify the result
        assert result is None
        mock_get_by_id.assert_called_once_with(user_id, todo_id)


def test_get_todo_by_id_invalid_user_id():
    """Test that getting a todo with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID
    todo_id = 1

    with pytest.raises(TodoValidationError):
        service.get_todo_by_id(user_id, todo_id)


def test_get_todo_by_id_invalid_todo_id_negative():
    """Test that getting a todo with negative todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = -1  # Invalid todo ID

    with pytest.raises(TodoValidationError):
        service.get_todo_by_id(user_id, todo_id)


def test_get_todo_by_id_invalid_todo_id_zero():
    """Test that getting a todo with zero todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 0  # Invalid todo ID

    with pytest.raises(TodoValidationError):
        service.get_todo_by_id(user_id, todo_id)


def test_get_todo_by_id_invalid_todo_id_string():
    """Test that getting a todo with string todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = "invalid"  # Invalid todo ID type

    with pytest.raises(TodoValidationError):
        service.get_todo_by_id(user_id, todo_id)


def test_get_todo_by_id_none_user_id():
    """Test that getting a todo with None user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = None  # Invalid user ID
    todo_id = 1

    with pytest.raises(TodoValidationError):
        service.get_todo_by_id(user_id, todo_id)


if __name__ == "__main__":
    pytest.main([__file__])