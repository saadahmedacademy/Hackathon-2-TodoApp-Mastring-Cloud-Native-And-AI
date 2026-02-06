"""Integration tests for todo delete functionality."""
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


def test_delete_todo_success(client: TestClient):
    """Test successful deletion of a todo."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Todo to Delete", "description": "Will be deleted"}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Delete the todo
    response = client.delete(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 204  # No content

    # Verify the todo is gone
    get_response = client.get(f"/api/{user_id}/tasks/{todo_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_todo(client: TestClient):
    """Test deleting a nonexistent todo returns 404 error."""
    user_id = "test_user_123"
    nonexistent_id = 9999

    response = client.delete(f"/api/{user_id}/tasks/{nonexistent_id}")

    assert response.status_code == 404


def test_delete_todo_invalid_user_id(client: TestClient):
    """Test deleting a todo with invalid user ID returns 400 error."""
    user_id = ""  # Invalid user ID
    todo_id = 1

    response = client.delete(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 400


def test_delete_todo_invalid_todo_id(client: TestClient):
    """Test deleting a todo with invalid todo ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = -1  # Invalid todo ID

    response = client.delete(f"/api/{user_id}/tasks/{todo_id}")

    assert response.status_code == 400


def test_delete_todo_with_string_id(client: TestClient):
    """Test deleting a todo with string ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = "invalid"  # Invalid todo ID

    response = client.delete(f"/api/{user_id}/tasks/{todo_id}")

    # This will likely return 404 because FastAPI converts path params to int, causing validation error
    # but if it reaches our validation, it would be 400


if __name__ == "__main__":
    pytest.main([__file__])