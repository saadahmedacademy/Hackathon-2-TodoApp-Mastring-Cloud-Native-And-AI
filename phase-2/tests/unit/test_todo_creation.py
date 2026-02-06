"""Unit tests for todo creation functionality."""
import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.models.todo import TodoCreate
from src.services.todo_service import TodoService
from src.exceptions.base import TodoValidationError
from src.utils.validation import validate_todo_title


def test_validate_todo_title_valid():
    """Test that validate_todo_title returns True for valid titles."""
    assert validate_todo_title("Valid title")
    assert validate_todo_title("A" * 255)  # Maximum length


def test_validate_todo_title_invalid():
    """Test that validate_todo_title returns False for invalid titles."""
    assert not validate_todo_title("")  # Empty string
    assert not validate_todo_title(None)  # None value
    assert not validate_todo_title("   ")  # Whitespace only
    assert not validate_todo_title("A" * 256)  # Too long


def test_create_todo_success():
    """Test successful creation of a todo."""
    # Mock the database session
    mock_session = Mock(spec=Session)

    # Create a service instance
    service = TodoService(mock_session)

    # Mock the repository's create_todo method to return a dummy todo
    with patch.object(service.repository, 'create_todo') as mock_create:
        expected_todo = Mock()
        expected_todo.id = 1
        expected_todo.title = "Test Todo"
        expected_todo.description = "Test Description"
        expected_todo.completed = False
        expected_todo.user_id = "user123"

        mock_create.return_value = expected_todo

        # Create a todo
        user_id = "user123"
        todo_data = TodoCreate(title="Test Todo", description="Test Description")

        result = service.create_todo(user_id, todo_data)

        # Verify the result
        assert result == expected_todo
        mock_create.assert_called_once_with(user_id, todo_data)


def test_create_todo_invalid_user_id():
    """Test that creating a todo with invalid user ID raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = ""  # Invalid user ID
    todo_data = TodoCreate(title="Test Todo", description="Test Description")

    with pytest.raises(TodoValidationError):
        service.create_todo(user_id, todo_data)


def test_create_todo_empty_title():
    """Test that creating a todo with empty title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_data = TodoCreate(title="", description="Test Description")

    with pytest.raises(TodoValidationError):
        service.create_todo(user_id, todo_data)


def test_create_todo_whitespace_title():
    """Test that creating a todo with whitespace-only title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_data = TodoCreate(title="   ", description="Test Description")

    with pytest.raises(TodoValidationError):
        service.create_todo(user_id, todo_data)


def test_create_todo_long_title():
    """Test that creating a todo with too-long title raises ValidationError."""
    mock_session = Mock(spec=Session)
    service = TodoService(mock_session)

    user_id = "user123"
    todo_data = TodoCreate(title="A" * 256, description="Test Description")  # Too long

    with pytest.raises(TodoValidationError):
        service.create_todo(user_id, todo_data)


if __name__ == "__main__":
    pytest.main([__file__])