from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from src.main import app # Assuming main.py is in the root of src
from src.db.session import get_db
from src.db.base import BaseSQLModel
from src.models.task import Task
from datetime import datetime, timezone # Import timezone
import json

# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)
    
    connection = test_engine.connect()
    transaction = connection.begin()
    
    with Session(bind=connection) as session:
        yield session
        
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    
    app.dependency_overrides[get_db] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear() # Clear overrides after test

def test_add_task_api(client: TestClient, session: Session):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    description = "Buy groceries"
    due_date = "2026-02-15T18:00:00Z"

    response = client.post(
        f"/api/tasks/{user_id}/add",
        json={"description": description, "due_date": due_date}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert "task_id" in response_data
    assert response_data["description"] == description

    task = session.get(Task, UUID(response_data["task_id"]))
    assert task is not None
    assert task.user_id == user_id
    assert task.description == description
    assert task.status == "pending"
    # Convert both datetimes to timezone-aware UTC for consistent comparison
    expected_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00")).astimezone(timezone.utc)
    actual_due_date = task.due_date.replace(tzinfo=timezone.utc) if task.due_date.tzinfo is None else task.due_date.astimezone(timezone.utc)
    assert actual_due_date == expected_due_date

def test_add_task_api_missing_description(client: TestClient):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    response = client.post(
        f"/api/tasks/{user_id}/add",
        json={}
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

def test_add_task_api_invalid_user_id(client: TestClient):
    response = client.post(
        "/api/tasks/invalid-uuid/add",
        json={"description": "Test task"}
    )
    assert response.status_code == 422 # Unprocessable Entity for UUID validation error

def test_list_tasks_api(client: TestClient, session: Session):
    user_id = UUID("b1b2c3d4-e5f6-7890-1234-567890abcdef") # New user for this test
    client.post(f"/api/tasks/{user_id}/add", json={"description": "Task 1 for list"})
    client.post(f"/api/tasks/{user_id}/add", json={"description": "Task 2 for list", "status": "completed"})

    response = client.get(f"/api/tasks/{user_id}/list")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert len(response_data["tasks"]) == 2
    assert response_data["tasks"][0]["description"] == "Task 1 for list"
    assert response_data["tasks"][1]["description"] == "Task 2 for list"

def test_list_tasks_api_filtered_by_status(client: TestClient, session: Session):
    user_id = UUID("c1c2c3d4-e5f6-7890-1234-567890abcdef") # New user for this test
    client.post(f"/api/tasks/{user_id}/add", json={"description": "Task for filter 1", "status": "pending"})
    client.post(f"/api/tasks/{user_id}/add", json={"description": "Task for filter 2", "status": "completed"})

    response = client.get(f"/api/tasks/{user_id}/list?status=pending")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert len(response_data["tasks"]) == 1
    assert response_data["tasks"][0]["description"] == "Task for filter 1"
    assert response_data["tasks"][0]["status"] == "pending"
