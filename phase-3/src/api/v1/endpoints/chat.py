from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from src.db.session import get_db
from src.services.conversation_service import ConversationService
from src.agents.base import AIAgentBase, AgentRateLimitError
from src.config import settings
from src.repositories.todo_repository import TodoRepository
from src.utils.security import validate_user_id

router = APIRouter()


# ── Request models ─────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


# ── Agent dependency — registers all MCP tools on every request ────────────────
def get_ai_agent() -> AIAgentBase:
    from src.mcp.tools.add_task import add_task_tool_schema
    from src.mcp.tools.list_tasks import list_tasks_tool_schema
    from src.mcp.tools.complete_task import complete_task_tool_schema
    from src.mcp.tools.delete_task import delete_task_tool_schema
    from src.mcp.tools.update_task import update_task_tool_schema

    agent = AIAgentBase()
    for schema in [
        add_task_tool_schema,
        list_tasks_tool_schema,
        complete_task_tool_schema,
        delete_task_tool_schema,
        update_task_tool_schema,
    ]:
        agent.tools.append(schema)
    return agent


# ── Chat endpoint ──────────────────────────────────────────────────────────────
@router.post(
    "/api/{user_id}/chat",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def chat_with_ai(
    user_id: UUID,
    chat_message: ChatMessage,
    db: Session = Depends(get_db),
    ai_agent: AIAgentBase = Depends(get_ai_agent),
):
    user_id = validate_user_id(user_id)
    if not chat_message.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty",
        )
    try:
        conversation_service = ConversationService(session=db, ai_agent=ai_agent)
        response_data = conversation_service.send_message_to_agent(
            user_id, chat_message.conversation_id, chat_message.message
        )
        return response_data
    except AgentRateLimitError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}",
        )


# ── Todos listing endpoint ─────────────────────────────────────────────────────
# Returns todos WITH display_id so the frontend can show clean task numbers.
# Phase-2's /api/tasks endpoint does NOT include display_id in its response
# (it's excluded from Phase-2's TodoRead schema). This endpoint fills that gap.
@router.get(
    "/api/{user_id}/todos",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
)
async def list_todos_with_display_id(
    user_id: UUID,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """
    Return todos for a user including display_id.
    Used by the frontend after migration to ensure display_id is always visible.
    """
    user_id = validate_user_id(user_id)
    repo = TodoRepository(db)
    try:
        todos = repo.get_all(user_id=user_id, completed=completed)
        return [
            {
                "id": t.id,
                "display_id": t.display_id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed,
                "user_id": t.user_id,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "updated_at": t.updated_at.isoformat() if t.updated_at else None,
            }
            for t in todos
        ]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch todos: {e}",
        )
