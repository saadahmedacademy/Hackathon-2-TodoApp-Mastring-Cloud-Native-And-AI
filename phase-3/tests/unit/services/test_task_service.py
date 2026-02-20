from uuid import UUID
import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from datetime import datetime

from src.models.task import Task
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_task_repo():
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def task_service(mock_session, mock_task_repo):
    service = TaskService(session=mock_session)
    service.task_repo = mock_task_repo  # Inject mocked repo
    return service


@pytest.fixture
def user_id():
    return UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")


@pytest.fixture
def task_id():
    return UUID("f1f2f3f4-e5f6-7890-1234-567890abcdef")


@patch('src.services.task_service.add_task_tool')
def test_add_task_service(
    mock_add_task_tool: MagicMock,
    task_service: TaskService,
    user_id: UUID,
    task_id: UUID
):
    # Mock the return value of add_task_tool
    mock_add_task_tool.return_value = {
        "status": "success",
        "task_id": str(task_id),
        "description": "New Task",
        "user_id": str(user_id)
    }
    
    description = "New Task"
    result = task_service.add_task(user_id, description)
    
    mock_add_task_tool.assert_called_once_with(task_service.session, user_id, description, None, None)
    assert result["status"] == "success"
    assert result["description"] == "New Task"


@patch('src.services.task_service.list_tasks_tool')
def test_list_tasks_service(
    mock_list_tasks_tool: MagicMock,
    task_service: TaskService,
    user_id: UUID,
    task_id: UUID
):
    # Mock the return value of list_tasks_tool
    mock_list_tasks_tool.return_value = {
        "status": "success",
        "tasks": [
            {"id": str(task_id), "user_id": str(user_id), "description": "Task 1", "status": "pending"},
            {"id": "b1b2c3d4-e5f6-7890-1234-567890abcde0", "user_id": str(user_id), "description": "Task 2", "status": "completed"}
        ]
    }
    
    result = task_service.list_tasks(user_id)
    
    mock_list_tasks_tool.assert_called_once_with(task_service.session, user_id, None)
    assert result["status"] == "success"
    assert len(result["tasks"]) == 2


@patch('src.services.task_service.complete_task_tool')
def test_complete_task_service(
    mock_complete_task_tool: MagicMock,
    task_service: TaskService,
    user_id: UUID,
    task_id: UUID
):
    # Mock the return value of complete_task_tool
    mock_complete_task_tool.return_value = {
        "status": "success",
        "task_id": str(task_id),
        "new_status": "completed"
    }

    result = task_service.complete_task(user_id, task_id)

    mock_complete_task_tool.assert_called_once_with(task_service.session, user_id, task_id)
    assert result["status"] == "success"
    assert result["new_status"] == "completed"


@patch('src.services.task_service.delete_task_tool')
def test_delete_task_service(
    mock_delete_task_tool: MagicMock,
    task_service: TaskService,
    user_id: UUID,
    task_id: UUID
):
    # Mock the return value of delete_task_tool
    mock_delete_task_tool.return_value = {
        "status": "success",
        "task_id": str(task_id)
    }

    result = task_service.delete_task(user_id, task_id)

    mock_delete_task_tool.assert_called_once_with(task_service.session, user_id, task_id)
    assert result["status"] == "success"


@patch('src.services.task_service.update_task_tool')
def test_update_task_service(
    mock_update_task_tool: MagicMock,
    task_service: TaskService,
    user_id: UUID,
    task_id: UUID
):
    # Mock the return value of update_task_tool
    mock_update_task_tool.return_value = {
        "status": "success",
        "task_id": str(task_id),
        "description": "New Description",
        "new_status": "in_progress"
    }

    result = task_service.update_task(user_id, task_id, description="New Description", status="in_progress")

    mock_update_task_tool.assert_called_once_with(
        task_service.session, user_id, task_id, description="New Description", status="in_progress", due_date=None
    )
    assert result["status"] == "success"
    assert result["description"] == "New Description"
    assert result["new_status"] == "in_progress"
