"""Integration tests for todo retrieval functionality."""
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


def test_get_todo_by_id_success(client: TestClient):
    """Test successful retrieval of a todo by ID."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Todo to Retrieve", "description": "Will be retrieved"}
    )

    assert create_response.status_code == 201
    created_data = create_response.json()
    todo_id = created_data["id"]

    # Get the todo by ID
    response = client.get(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Todo to Retrieve"
    assert data["description"] == "Will be retrieved"
    assert data["completed"] is False
    assert data["user_id"] == user_id


def test_get_nonexistent_todo_by_id(client: TestClient):
    """Test retrieving a nonexistent todo by ID returns 404 error."""
    user_id = "test_user_123"
    nonexistent_id = 9999

    response = client.get(f"/api/{user_id}/tasks/{nonexistent_id}")

    assert response.status_code == 404


def test_get_todo_by_id_invalid_user_id(client: TestClient):
    """Test retrieving a todo with invalid user ID returns 400 error."""
    user_id = ""  # Invalid user ID
    todo_id = 1

    response = client.get(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 400


def test_get_todo_by_id_invalid_todo_id(client: TestClient):
    """Test retrieving a todo with invalid todo ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = -1  # Invalid todo ID

    response = client.get(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 400


def test_get_todo_by_id_zero_id(client: TestClient):
    """Test retrieving a todo with zero ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = 0  # Invalid todo ID

    response = client.get(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__])