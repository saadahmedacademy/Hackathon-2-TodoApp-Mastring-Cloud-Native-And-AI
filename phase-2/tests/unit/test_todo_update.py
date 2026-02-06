"""Unit tests for todo update functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.todo_service import TodoService
from src.models.todo import Todo, TodoUpdate
from src.exceptions.base import TodoValidationError


def test_update_todo_success():
    """Test successful updating of a todo."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's update_todo method to return a dummy todo
    with patch.object(service.repository, 'update_todo') as mock_update:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Updated Todo"
        expected_todo.description = "Updated Description"
        expected_todo.completed = True
        expected_todo.user_id = "user123"

        mock_update.return_value = expected_todo

        # Update a todo
        user_id = "user123"
        todo_id = 1
        todo_data = TodoUpdate(title="Updated Todo", description="Updated Description", completed=True)

        result = service.update_todo(user_id, todo_id, todo_data)

        # Verify the result
        assert result == expected_todo
        mock_update.assert_called_once_with(user_id, todo_id, todo_data)


def test_update_todo_partial_fields():
    """Test updating a todo with partial field updates."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    with patch.object(service.repository, 'update_todo') as mock_update:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Partially Updated Todo"
        expected_todo.description = "Original Description"
        expected_todo.completed = False
        expected_todo.user_id = "user123"

        mock_update.return_value = expected_todo

        # Update only the title
        user_id = "user123"
        todo_id = 1
        todo_data = TodoUpdate(title="Partially Updated Todo")

        result = service.update_todo(user_id, todo_id, todo_data)

        # Verify the result
        assert result == expected_todo
        mock_update.assert_called_once_with(user_id, todo_id, todo_data)


def test_update_todo_invalid_user_id():
    """Test that updating a todo with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID
    todo_id = 1
    todo_data = TodoUpdate(title="Updated Todo")

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


def test_update_todo_invalid_todo_id():
    """Test that updating a todo with invalid todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = -1  # Invalid todo ID
    todo_data = TodoUpdate(title="Updated Todo")

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


def test_update_todo_empty_title():
    """Test that updating a todo with empty title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    todo_data = TodoUpdate(title="")  # Empty title

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


def test_update_todo_whitespace_title():
    """Test that updating a todo with whitespace-only title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    todo_data = TodoUpdate(title="   ")  # Whitespace-only title

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


def test_update_todo_long_title():
    """Test that updating a todo with too-long title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    todo_data = TodoUpdate(title="A" * 256)  # Too long title

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


def test_update_todo_long_description():
    """Test that updating a todo with too-long description raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    todo_data = TodoUpdate(description="A" * 1001)  # Too long description

    with pytest.raises(TodoValidationError):
        service.update_todo(user_id, todo_id, todo_data)


if __name__ == "__main__":
    pytest.main([__file__])