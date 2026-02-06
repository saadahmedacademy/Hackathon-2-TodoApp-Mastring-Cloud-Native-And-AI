"""
TodoItem and TodoList models for the console todo application.
"""
from typing import List, Optional


class TodoItem:
    """
    Represents a single todo item with an ID, title, description, and completion status.
    """

    def __init__(self, id: int, title: str, description: Optional[str] = None):
        """
        Initialize a TodoItem.

        Args:
            id: Unique identifier for the todo item
            title: Title of the todo item (required)
            description: Optional description of the todo item
        """
        self.id = id
        self.title = title
        self.description = description
        self.completed = False

    def __str__(self):
        """Return a string representation of the todo item."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title}"

    def __repr__(self):
        """Return a detailed string representation of the todo item."""
        return f"TodoItem(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"


class TodoList:
    """
    Collection of TodoItem objects with methods to manage them.
    """

    def __init__(self):
        """Initialize an empty TodoList with next_id counter."""
        self.items: List[TodoItem] = []
        self.next_id = 1

    def add_item(self, title: str, description: Optional[str] = None) -> TodoItem:
        """
        Add a new todo item to the list.

        Args:
            title: Title of the todo item (required)
            description: Optional description of the todo item

        Returns:
            The newly created TodoItem
        """
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        todo_item = TodoItem(self.next_id, title.strip(), description)
        self.items.append(todo_item)
        self.next_id += 1
        return todo_item

    def get_all_items(self) -> List[TodoItem]:
        """
        Get all todo items in the list.

        Returns:
            List of all TodoItem objects
        """
        return self.items.copy()

    def find_by_id(self, id: int) -> Optional[TodoItem]:
        """
        Find a todo item by its ID.

        Args:
            id: ID of the todo item to find

        Returns:
            TodoItem if found, None otherwise
        """
        for item in self.items:
            if item.id == id:
                return item
        return None

    def update_item(self, id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing todo item.

        Args:
            id: ID of the todo item to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            True if the item was updated, False if not found
        """
        item = self.find_by_id(id)
        if item is None:
            return False

        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            item.title = title.strip()

        if description is not None:
            item.description = description

        return True

    def mark_complete(self, id: int) -> bool:
        """
        Mark a todo item as complete.

        Args:
            id: ID of the todo item to mark complete

        Returns:
            True if the item was marked complete, False if not found
        """
        item = self.find_by_id(id)
        if item is None:
            return False

        item.completed = True
        return True

    def mark_incomplete(self, id: int) -> bool:
        """
        Mark a todo item as incomplete.

        Args:
            id: ID of the todo item to mark incomplete

        Returns:
            True if the item was marked incomplete, False if not found
        """
        item = self.find_by_id(id)
        if item is None:
            return False

        item.completed = False
        return True

    def delete_item(self, id: int) -> bool:
        """
        Delete a todo item from the list.

        Args:
            id: ID of the todo item to delete

        Returns:
            True if the item was deleted, False if not found
        """
        item = self.find_by_id(id)
        if item is None:
            return False

        self.items.remove(item)
        return True