from uuid import UUID
import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session, create_engine, SQLModel
from datetime import datetime

from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.mcp.tools.add_task import add_task_tool
from src.mcp.tools.list_tasks import list_tasks_tool
from src.mcp.tools.complete_task import complete_task_tool
from src.mcp.tools.delete_task import delete_task_tool
from src.mcp.tools.update_task import update_task_tool


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def mock_task_repo():
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def user_id():
    return UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")


def test_add_task_tool(session: Session, user_id: UUID):
    result = add_task_tool(session, user_id, "Buy groceries")
    assert result["status"] == "success"
    assert "task_id" in result
    assert "description" in result

    task = session.get(Task, UUID(result["task_id"]))
    assert task is not None
    assert task.user_id == user_id
    assert task.description == "Buy groceries"


def test_list_tasks_tool(session: Session, user_id: UUID):
    add_task_tool(session, user_id, "Task 1")
    add_task_tool(session, user_id, "Task 2")
    add_task_tool(session, UUID("b1b2c3d4-e5f6-7890-1234-567890abcdef"), "Other User Task")

    result = list_tasks_tool(session, user_id)
    assert result["status"] == "success"
    assert len(result["tasks"]) == 2
    assert result["tasks"][0]["description"] == "Task 1"
    assert result["tasks"][1]["description"] == "Task 2"

    result_filtered = list_tasks_tool(session, user_id, status="pending")
    assert len(result_filtered["tasks"]) == 2


def test_complete_task_tool(session: Session, user_id: UUID):
    task_result = add_task_tool(session, user_id, "Task to complete")
    task_id = UUID(task_result["task_id"])

    result = complete_task_tool(session, user_id, task_id)
    assert result["status"] == "success"
    assert result["new_status"] == "completed"

    task = session.get(Task, task_id)
    assert task.status == "completed"


def test_delete_task_tool(session: Session, user_id: UUID):
    task_result = add_task_tool(session, user_id, "Task to delete")
    task_id = UUID(task_result["task_id"])

    result = delete_task_tool(session, user_id, task_id)
    assert result["status"] == "success"
    assert result["task_id"] == str(task_id)

    task = session.get(Task, task_id)
    assert task is None


def test_update_task_tool(session: Session, user_id: UUID):
    task_result = add_task_tool(session, user_id, "Task to update", due_date=datetime(2026, 2, 12))
    task_id = UUID(task_result["task_id"])

    new_description = "Updated description"
    new_status = "in_progress"
    new_due_date = datetime(2026, 3, 1)

    result = update_task_tool(session, user_id, task_id, description=new_description, status=new_status, due_date=new_due_date)
    assert result["status"] == new_status
    assert result["description"] == new_description
    assert result["status"] == new_status
    assert result["due_date"] == new_due_date.isoformat()

    task = session.get(Task, task_id)
    assert task.description == new_description
    assert task.status == new_status
    assert task.due_date == new_due_date