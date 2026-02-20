"""
MCP Tool: list_tasks_tool
Lists todos from the shared 'todo' table for the current user.
Returns display_id instead of raw PK — never exposes UUIDs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from sqlmodel import Session

from src.repositories.todo_repository import TodoRepository


def list_tasks_tool(
    session: Session,
    user_id: Union[UUID, str],
    status: Optional[str] = None,
    **_kwargs: Any,
) -> Dict[str, Any]:
    """
    List tasks for the user, optionally filtered by completion status.

    Args:
        session:  Active database session.
        user_id:  Owning user (UUID or str).
        status:   Optional filter — "pending" | "completed".

    Returns:
        {"status": "success", "tasks": [{"display_id": int, "title": str, "completed": bool}, ...]}
        {"status": "error",   "message": str}
    """
    repo = TodoRepository(session)
    try:
        # Expire cached data to ensure fresh read after any previous writes
        session.expire_all()

        # Map human-friendly status string to the boolean field
        completed_filter: Optional[bool] = None
        if status == "completed":
            completed_filter = True
        elif status == "pending":
            completed_filter = False

        todos = repo.get_all(user_id=user_id, completed=completed_filter)

        tasks: List[Dict[str, Any]] = [
            {
                "display_id": t.display_id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
            }
            for t in todos
        ]
        return {"status": "success", "tasks": tasks}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


# ── OpenAI tool schema ─────────────────────────────────────────────────────────
list_tasks_tool_schema = {
    "type": "function",
    "function": {
        "name": "list_tasks_tool",
        "description": (
            "Lists tasks for the current user. "
            "Optionally filter by status ('pending' or 'completed')."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["pending", "completed"],
                    "description": "Filter tasks by completion status.",
                },
            },
            "required": [],
        },
    },
}
