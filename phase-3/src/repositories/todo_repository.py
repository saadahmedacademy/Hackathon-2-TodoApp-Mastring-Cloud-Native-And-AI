"""
TodoRepository for Phase-3.

Operates exclusively on the shared 'todo' table.
Accepts user_id as UUID | str and normalises to str for DB comparisons,
matching Phase-2's convention of storing user_id as a UUID string.
"""

from __future__ import annotations

from typing import List, Optional, Union
from uuid import UUID

from sqlmodel import Session, func, select

from src.models.todo import Todo


def _uid(user_id: Union[UUID, str]) -> str:
    """Normalise user_id to the str format used in the todo table."""
    return str(user_id)


class TodoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------ #
    #  display_id helpers                                                  #
    # ------------------------------------------------------------------ #

    def _next_display_id(self, user_id: str) -> int:
        """Return the next sequential display_id for this user."""
        result = self.session.exec(
            select(func.max(Todo.display_id)).where(Todo.user_id == user_id)
        ).first()
        return (result or 0) + 1

    # ------------------------------------------------------------------ #
    #  CRUD                                                                #
    # ------------------------------------------------------------------ #

    def create(
        self,
        user_id: Union[UUID, str],
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Todo:
        """
        Create a new todo.

        If `title` is None or empty the row is saved as "Task {display_id}",
        keeping the column's min_length=1 constraint satisfied.
        """
        uid = _uid(user_id)
        display_id = self._next_display_id(uid)
        # Auto-generate title when caller omits it (e.g. plain-sentence input)
        actual_title = (title.strip() if title and title.strip() else f"Task {display_id}")
        todo = Todo(
            user_id=uid,
            title=actual_title,
            description=description,
            completed=False,
            display_id=display_id,
        )
        self.session.add(todo)
        self.session.flush()
        self.session.refresh(todo)
        return todo

    def get_by_display_id(
        self, user_id: Union[UUID, str], display_id: int
    ) -> Optional[Todo]:
        uid = _uid(user_id)
        return self.session.exec(
            select(Todo).where(Todo.user_id == uid, Todo.display_id == display_id)
        ).first()

    def get_all(
        self,
        user_id: Union[UUID, str],
        completed: Optional[bool] = None,
    ) -> List[Todo]:
        uid = _uid(user_id)
        query = select(Todo).where(Todo.user_id == uid)
        if completed is not None:
            query = query.where(Todo.completed == completed)
        return self.session.exec(query.order_by(Todo.display_id)).all()

    def update(self, todo: Todo) -> Todo:
        from datetime import datetime, timezone

        todo.updated_at = datetime.now(timezone.utc)
        self.session.add(todo)
        self.session.flush()
        self.session.refresh(todo)
        return todo

    def delete(self, todo: Todo) -> None:
        self.session.delete(todo)
        self.session.flush()
