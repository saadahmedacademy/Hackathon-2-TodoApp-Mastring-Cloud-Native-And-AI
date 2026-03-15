"""
MCP Tool: delete_all_tasks_tool
Deletes all tasks for the current user.
"""

from __future__ import annotations

from typing import Any, Dict, Union
from uuid import UUID

from sqlmodel import Session

from src.repositories.todo_repository import TodoRepository


def delete_all_tasks_tool(
    session: Session,
    user_id: Union[UUID, str],
    **_kwargs: Any
) -> Dict[str, Any]:
    """
    Delete all tasks for a user.

    Args:
        session: Database session
        user_id: User UUID or string
        **_kwargs: Additional keyword arguments (ignored)

    Returns:
        Dictionary with status, deleted_count, and message
    """
    try:
        repo = TodoRepository(session)

        # Get all tasks for the user
        todos = repo.get_all(user_id)

        if not todos:
            return {
                "status": "success",
                "deleted_count": 0,
                "message": "No tasks found to delete."
            }

        # Delete all tasks
        deleted_count = 0
        for todo in todos:
            repo.delete(todo)
            deleted_count += 1

        # Commit all deletions
        session.commit()

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "message": f"Successfully deleted all {deleted_count} task(s)."
        }

    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "message": f"Failed to delete tasks: {str(e)}"
        }


# ── OpenAI tool schema ─────────────────────────────────────────────────────────
DELETE_ALL_TASKS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_all_tasks_tool",
        "description": "Delete all tasks for the current user. Use this when the user asks to delete all tasks, clear all tasks, or remove everything.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
