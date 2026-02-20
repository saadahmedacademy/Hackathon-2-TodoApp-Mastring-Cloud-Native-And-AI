"""
MCP Tool: add_task_tool

Creates a new todo in the shared 'todo' table.

Calling conventions:
  - Explicit title + description: agent passes both fields.
  - Implicit (sentence only): agent passes description only; title is omitted.
    Repository auto-generates title as "Task {display_id}".

COMMAND CLEANING: the agent must strip command words (see system prompt) before
calling this tool. The tool itself does NOT perform command cleaning.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional, Union
from uuid import UUID

from sqlmodel import Session

from src.repositories.todo_repository import TodoRepository

# Prefixes the agent or user might leak into the description field
_COMMAND_PREFIXES = re.compile(
    r"^\s*(add\s+todo|create\s+todo|add\s+task|create\s+task)\s*:?\s*",
    re.IGNORECASE,
)


def _clean(text: Optional[str]) -> Optional[str]:
    """Strip leading command words from a string."""
    if not text:
        return text
    return _COMMAND_PREFIXES.sub("", text).strip() or None


def add_task_tool(
    session: Session,
    user_id: Union[UUID, str],
    description: str,
    title: Optional[str] = None,
    **_kwargs: Any,
) -> Dict[str, Any]:
    """
    Add a new task for the user.

    Args:
        session:     Active database session.
        user_id:     Owning user (UUID or str).
        description: Full content / body of the task.
        title:       Optional explicit title. When absent the repository
                     auto-generates "Task {display_id}".

    Returns:
        {"status": "success", "display_id": int, "title": str, "description": str | None}
        {"status": "error",   "message": str}
    """
    repo = TodoRepository(session)
    try:
        clean_title = _clean(title) or None
        clean_desc = _clean(description)

        todo = repo.create(
            user_id=user_id,
            title=clean_title,      # None → auto "Task N"
            description=clean_desc,
        )
        session.commit()
        session.refresh(todo)
        return {
            "status": "success",
            "display_id": todo.display_id,
            "title": todo.title,
            "description": todo.description,
        }
    except Exception as exc:
        session.rollback()
        return {"status": "error", "message": str(exc)}


# ── OpenAI tool schema ─────────────────────────────────────────────────────────
add_task_tool_schema = {
    "type": "function",
    "function": {
        "name": "add_task_tool",
        "description": (
            "Adds a new task for the current user.\n"
            "Pass 'title' when the user provides an explicit name.\n"
            "Pass only 'description' when the user gives a plain sentence — "
            "the system auto-generates a title like 'Task 3'.\n"
            "Always strip command words (add todo / create task / etc.) before passing."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": (
                        "Explicit task title (e.g. 'Grocery shopping'). "
                        "Omit if the user did not provide a distinct title."
                    ),
                },
                "description": {
                    "type": "string",
                    "description": (
                        "Full task content / description. "
                        "For plain-sentence input ('add todo buy milk') "
                        "this should be the cleaned sentence ('buy milk')."
                    ),
                },
            },
            "required": ["description"],
        },
    },
}
