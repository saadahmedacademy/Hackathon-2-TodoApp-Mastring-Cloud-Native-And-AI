"""
Unit tests for the console todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.models.todo import TodoList, TodoItem
from src.services.todo_service import TodoService


def test_todo_item_creation():
    """Test creating a TodoItem."""
    item = TodoItem(1, "Test title", "Test description")
    assert item.id == 1
    assert item.title == "Test title"
    assert item.description == "Test description"
    assert item.completed == False
    print("✓ TodoItem creation test passed")


def test_todo_list_add_item():
    """Test adding an item to TodoList."""
    todo_list = TodoList()
    item = todo_list.add_item("Test title", "Test description")

    assert len(todo_list.items) == 1
    assert item.id == 1
    assert item.title == "Test title"
    print("✓ TodoList add item test passed")


def test_todo_list_validation():
    """Test validation when adding items with empty titles."""
    todo_list = TodoList()
    try:
        todo_list.add_item("")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected
    print("✓ TodoList validation test passed")


def test_todo_service():
    """Test TodoService functionality."""
    service = TodoService()

    # Add a todo
    item = service.add_todo("Test todo", "Test description")
    assert item.id == 1
    assert item.title == "Test todo"

    # Get all todos
    todos = service.get_all_todos()
    assert len(todos) == 1

    # Update todo
    result = service.update_todo(1, "Updated title")
    assert result == True

    # Find by ID
    found_item = service.find_todo_by_id(1)
    assert found_item is not None
    assert found_item.title == "Updated title"

    # Mark complete
    result = service.mark_complete(1)
    assert result == True
    assert found_item.completed == True

    # Delete todo
    result = service.delete_todo(1)
    assert result == True
    assert len(service.get_all_todos()) == 0

    print("✓ TodoService test passed")


def run_tests():
    """Run all tests."""
    print("Running unit tests...")
    test_todo_item_creation()
    test_todo_list_add_item()
    test_todo_list_validation()
    test_todo_service()
    print("All tests passed! ✓")


if __name__ == "__main__":
    run_tests()