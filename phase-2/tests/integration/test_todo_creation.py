"""Integration tests for todo creation functionality."""
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


def test_create_todo_success(client: TestClient):
    """Test successful creation of a todo via API."""
    user_id = "test_user_123"
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Test Todo",
            "description": "Test Description"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert data["user_id"] == user_id
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_todo_without_description(client: TestClient):
    """Test creating a todo without description."""
    user_id = "test_user_123"
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Test Todo Without Description"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Todo Without Description"
    assert data["description"] is None
    assert data["user_id"] == user_id
    assert data["completed"] is False


def test_create_todo_missing_title(client: TestClient):
    """Test that creating a todo without title returns 422 error."""
    user_id = "test_user_123"
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "description": "This should fail without title"
        }
    )

    assert response.status_code == 422  # Validation error


def test_create_todo_empty_title(client: TestClient):
    """Test that creating a todo with empty title returns 422 error."""
    user_id = "test_user_123"
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "",
            "description": "This should fail with empty title"
        }
    )

    assert response.status_code == 422  # Validation error


def test_create_todo_invalid_user_id(client: TestClient):
    """Test that creating a todo with invalid user ID returns 400 error."""
    user_id = ""  # Invalid user ID
    response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Test Todo",
            "description": "Test Description"
        }
    )

    assert response.status_code == 400  # Bad request


if __name__ == "__main__":
    pytest.main([__file__])