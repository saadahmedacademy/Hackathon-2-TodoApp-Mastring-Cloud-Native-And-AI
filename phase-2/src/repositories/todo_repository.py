"""Repository layer for Todo database operations."""
from typing import List, Optional
from sqlmodel import select, Session, func
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..exceptions.base import TodoNotFoundException


class TodoRepository:
    """Repository class for handling all database operations related to Todo items."""

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        self.session = session

    def create_todo(self, user_id: str, todo_data: TodoCreate) -> Todo:
        """Create a new todo item for the specified user."""
        todo = Todo(
            user_id=user_id,
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed
        )
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_all_todos(self, user_id: str, completed: Optional[bool] = None) -> List[Todo]:
        """Get all todos for the specified user, optionally filtered by completion status."""
        query = select(Todo).where(Todo.user_id == user_id)

        if completed is not None:
            query = query.where(Todo.completed == completed)

        return self.session.exec(query).all()

    def get_todo_by_id(self, user_id: str, todo_id: int) -> Optional[Todo]:
        """Get a specific todo by ID for the specified user."""
        query = select(Todo).where(Todo.user_id == user_id, Todo.id == todo_id)
        return self.session.exec(query).first()

    def update_todo(self, user_id: str, todo_id: int, todo_data: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo for the specified user."""
        todo = self.get_todo_by_id(user_id, todo_id)
        if todo is None:
            return None

        # Update fields if they are provided in the update data
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.completed is not None:
            todo.completed = todo_data.completed

        # Update the timestamp
        from datetime import datetime, timezone
        todo.updated_at = datetime.now(timezone.utc)

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete_todo(self, user_id: str, todo_id: int) -> bool:
        """Delete a todo by ID for the specified user."""
        todo = self.get_todo_by_id(user_id, todo_id)
        if todo is None:
            return False

        self.session.delete(todo)
        self.session.commit()
        return True

    def mark_complete(self, user_id: str, todo_id: int, completed: bool) -> Optional[Todo]:
        """Mark a todo as complete or incomplete for the specified user."""
        todo = self.get_todo_by_id(user_id, todo_id)
        if todo is None:
            return None

        todo.completed = completed

        # Update the timestamp
        from datetime import datetime, timezone
        todo.updated_at = datetime.now(timezone.utc)

        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo