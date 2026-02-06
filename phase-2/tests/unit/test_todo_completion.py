"""Unit tests for todo completion functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.services.todo_service import TodoService
from src.models.todo import Todo
from src.exceptions.base import TodoValidationError


def test_mark_complete_success():
    """Test successful marking of a todo as complete."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's mark_complete method to return a dummy todo
    with patch.object(service.repository, 'mark_complete') as mock_mark_complete:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Test Todo"
        expected_todo.description = "Test Description"
        expected_todo.completed = True
        expected_todo.user_id = "user123"

        mock_mark_complete.return_value = expected_todo

        # Mark todo as complete
        user_id = "user123"
        todo_id = 1
        completed = True

        result = service.mark_complete(user_id, todo_id, completed)

        # Verify the result
        assert result == expected_todo
        mock_mark_complete.assert_called_once_with(user_id, todo_id, completed)


def test_mark_incomplete_success():
    """Test successful marking of a todo as incomplete."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    with patch.object(service.repository, 'mark_complete') as mock_mark_complete:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Test Todo"
        expected_todo.description = "Test Description"
        expected_todo.completed = False
        expected_todo.user_id = "user123"

        mock_mark_complete.return_value = expected_todo

        # Mark todo as incomplete
        user_id = "user123"
        todo_id = 1
        completed = False

        result = service.mark_complete(user_id, todo_id, completed)

        # Verify the result
        assert result == expected_todo
        mock_mark_complete.assert_called_once_with(user_id, todo_id, completed)


def test_mark_complete_invalid_user_id():
    """Test that marking a todo with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID
    todo_id = 1
    completed = True

    with pytest.raises(TodoValidationError):
        service.mark_complete(user_id, todo_id, completed)


def test_mark_complete_invalid_todo_id():
    """Test that marking a todo with invalid todo ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = -1  # Invalid todo ID

    with pytest.raises(TodoValidationError):
        service.mark_complete(user_id, todo_id, True)


def test_mark_complete_invalid_completed_param():
    """Test that marking a todo with non-boolean completed param raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    completed = "invalid"  # Invalid completed value

    with pytest.raises(TodoValidationError):
        service.mark_complete(user_id, todo_id, completed)


def test_mark_complete_none_completed_param():
    """Test that marking a todo with None completed param raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_id = 1
    completed = None  # Invalid completed value

    with pytest.raises(TodoValidationError):
        service.mark_complete(user_id, todo_id, completed)


if __name__ == "__main__":
    pytest.main([__file__])