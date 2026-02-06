"""
TodoService class for the console todo application.
Handles business logic for todo operations.
"""
from typing import List, Optional
from src.models.todo import TodoList, TodoItem


class TodoService:
    """
    Service class that handles all todo-related business logic.
    """

    def __init__(self):
        """Initialize the TodoService with a TodoList."""
        self.todo_list = TodoList()

    def add_todo(self, title: str, description: Optional[str] = None) -> TodoItem:
        """
        Add a new todo item.

        Args:
            title: Title of the todo item (required)
            description: Optional description of the todo item

        Returns:
            The newly created TodoItem

        Raises:
            ValueError: If title is empty or None
        """
        return self.todo_list.add_item(title, description)

    def get_all_todos(self) -> List[TodoItem]:
        """
        Get all todo items.

        Returns:
            List of all TodoItem objects
        """
        return self.todo_list.get_all_items()

    def update_todo(self, id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing todo item.

        Args:
            id: ID of the todo item to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the item was updated, False if not found

        Raises:
            ValueError: If title is empty
        """
        return self.todo_list.update_item(id, title, description)

    def mark_complete(self, id: int) -> bool:
        """
        Mark a todo item as complete.

        Args:
            id: ID of the todo item to mark complete

        Returns:
            True if the item was marked complete, False if not found
        """
        return self.todo_list.mark_complete(id)

    def mark_incomplete(self, id: int) -> bool:
        """
        Mark a todo item as incomplete.

        Args:
            id: ID of the todo item to mark incomplete

        Returns:
            True if the item was marked incomplete, False if not found
        """
        return self.todo_list.mark_incomplete(id)

    def delete_todo(self, id: int) -> bool:
        """
        Delete a todo item.

        Args:
            id: ID of the todo item to delete

        Returns:
            True if the item was deleted, False if not found
        """
        return self.todo_list.delete_item(id)

    def find_todo_by_id(self, id: int) -> Optional[TodoItem]:
        """
        Find a todo item by its ID.

        Args:
            id: ID of the todo item to find

        Returns:
            TodoItem if found, None otherwise
        """
        return self.todo_list.find_by_id(id)