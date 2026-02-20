"""
MCP Tool: update_task_tool
Updates a todo's title, description, or completion status using its display_id.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Union
from uuid import UUID

from sqlmodel import Session

from src.repositories.todo_repository import TodoRepository


def update_task_tool(
    session: Session,
    user_id: Union[UUID, str],
    display_id: int,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    **_kwargs: Any,
) -> Dict[str, Any]:
    """
    Update a task's title and/or completion status.

    Args:
        session:     Active database session.
        user_id:     Owning user (UUID or str).
        display_id:  User-scoped sequential task number.
        description: New title/description (optional).
        completed:   New completion state (optional).

    Returns:
        {"status": "success", "display_id": int, "title": str, "completed": bool}
        {"status": "error",   "message": str}
    """
    repo = TodoRepository(session)
    try:
        todo = repo.get_by_display_id(user_id, display_id)
        if todo is None:
            return {
                "status": "error",
                "message": f"Task #{display_id} not found.",
            }

        if description is not None:
            todo.title = description
        if completed is not None:
            todo.completed = completed

        repo.update(todo)
        session.commit()
        return {
            "status": "success",
            "display_id": todo.display_id,
            "title": todo.title,
            "completed": todo.completed,
        }
    except Exception as exc:
        session.rollback()
        return {"status": "error", "message": str(exc)}


# ── OpenAI tool schema ─────────────────────────────────────────────────────────
update_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "update_task_tool",
        "description": (
            "Updates an existing task's title or completion status using its display_id."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "display_id": {
                    "type": "integer",
                    "description": "The task's display number (e.g. 3 for Task #3).",
                },
                "description": {
                    "type": "string",
                    "description": "New title/description for the task.",
                },
                "completed": {
                    "type": "boolean",
                    "description": "Set true to mark as done, false to mark as pending.",
                },
            },
            "required": ["display_id"],
        },
    },
}
