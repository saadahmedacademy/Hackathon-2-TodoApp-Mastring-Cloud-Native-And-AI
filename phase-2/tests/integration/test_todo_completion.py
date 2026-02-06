"""Integration tests for todo completion functionality."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.api.main import app
from src.db.session import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_mark_todo_complete_success(client: TestClient):
    """Test successful marking of a todo as complete."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Test Todo", "description": "To be completed"}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Mark as complete
    response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] is True


def test_mark_todo_incomplete_success(client: TestClient):
    """Test successful marking of a todo as incomplete."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Test Todo", "description": "To be marked incomplete"}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Mark as complete first
    client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": True}
    )

    # Then mark as incomplete
    response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": False}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["completed"] is False


def test_mark_nonexistent_todo(client: TestClient):
    """Test marking a nonexistent todo returns 404 error."""
    user_id = "test_user_123"
    nonexistent_id = 9999

    response = client.patch(
        f"/api/{user_id}/tasks/{nonexistent_id}/complete",
        params={"completed": True}
    )

    assert response.status_code == 404


def test_mark_todo_invalid_user_id(client: TestClient):
    """Test marking a todo with invalid user ID returns 400 error."""
    user_id = ""  # Invalid user ID
    todo_id = 1

    response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": True}
    )

    assert response.status_code == 400


def test_mark_todo_invalid_todo_id(client: TestClient):
    """Test marking a todo with invalid todo ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = -1  # Invalid todo ID

    response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": True}
    )

    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__])