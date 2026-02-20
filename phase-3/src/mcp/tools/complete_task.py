"""
MCP Tool: complete_task_tool
Marks a todo as completed using its user-scoped display_id.
"""

from __future__ import annotations

from typing import Any, Dict, Union
from uuid import UUID

from sqlmodel import Session

from src.repositories.todo_repository import TodoRepository


def complete_task_tool(
    session: Session,
    user_id: Union[UUID, str],
    display_id: int,
    **_kwargs: Any,
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        session:    Active database session.
        user_id:    Owning user (UUID or str).
        display_id: User-scoped sequential task number.

    Returns:
        {"status": "success", "display_id": int, "title": str}
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

        todo.completed = True
        repo.update(todo)
        session.commit()
        return {
            "status": "success",
            "display_id": todo.display_id,
            "title": todo.title,
        }
    except Exception as exc:
        session.rollback()
        return {"status": "error", "message": str(exc)}


# ── OpenAI tool schema ─────────────────────────────────────────────────────────
complete_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "complete_task_tool",
        "description": "Marks a task as completed using its display_id number.",
        "parameters": {
            "type": "object",
            "properties": {
                "display_id": {
                    "type": "integer",
                    "description": "The task's display number (e.g. 3 for Task #3).",
                },
            },
            "required": ["display_id"],
        },
    },
}
