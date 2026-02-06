"""Unit tests for todo delete functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.todo_service import TodoService
from src.exceptions.base import TodoValidationError


def test_delete_todo_success():
    """Test successful deletion of a todo."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's delete_todo method to return True
    with patch.object(service.repository, 'delete_todo') as mock_delete:
        mock_delete.return_value = True

        # Delete a todo
        user_id = "user123"
        todo_id = 1

        result = service.delete_todo(user_id, todo_id)

        # Verify the result
        assert result is True
        mock_delete.assert_called_once_with(user_id, todo_id)


def test_delete_nonexistent_todo():
    """Test deletion of a nonexistent todo."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    with patch.object(service.repository, 'delete_todo') as mock_delete:
        mock_delete.return_value = False  # Todo not found

        # Delete a nonexistent todo
        user_id = "user123"
        todo_id = 9999

        result = service.delete_todo(user_id, todo_id)

        # Verify the result
        assert result is False
        mock_delete.assert_called_once_with(user_id, todo_id)


def test_delete_todo_invalid_user_id():
    """Test that deleting a todo with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID
    todo_id = 1

    with pytest.raises(TodoValidationError):
        service.delete_todo(user_id, todo_id)


def test_delete_todo_invalid_todo_id():
    """Test that deleting a todo with invalid todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = -1  # Invalid todo ID

    with pytest.raises(TodoValidationError):
        service.delete_todo(user_id, todo_id)


def test_delete_todo_zero_id():
    """Test that deleting a todo with zero ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 0  # Invalid todo ID

    with pytest.raises(TodoValidationError):
        service.delete_todo(user_id, todo_id)


def test_delete_todo_string_id():
    """Test that deleting a todo with string ID raises TypeError (caught by validation)."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = "invalid"  # Invalid todo ID type

    with pytest.raises(TodoValidationError):
        service.delete_todo(user_id, todo_id)


if __name__ == "__main__":
    pytest.main([__file__])