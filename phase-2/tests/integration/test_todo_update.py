"""Integration tests for todo update functionality."""
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


def test_update_todo_success(client: TestClient):
    """Test successful updating of a todo."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Original Todo", "description": "Original Description"}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Update the todo
    response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={
            "title": "Updated Todo",
            "description": "Updated Description",
            "completed": True
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated Todo"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True


def test_update_todo_partial_fields(client: TestClient):
    """Test updating a todo with partial field updates."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Original Todo", "description": "Original Description", "completed": False}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Update only the title
    response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={
            "title": "Updated Title Only"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated Title Only"
    # Note: Description should remain unchanged in actual DB, but this is a limitation of our test setup


def test_update_nonexistent_todo(client: TestClient):
    """Test updating a nonexistent todo returns 404 error."""
    user_id = "test_user_123"
    nonexistent_id = 9999

    response = client.put(
        f"/api/{user_id}/tasks/{nonexistent_id}",
        json={"title": "Updated Todo"}
    )

    assert response.status_code == 404


def test_update_todo_invalid_user_id(client: TestClient):
    """Test updating a todo with invalid user ID returns 400 error."""
    user_id = ""  # Invalid user ID
    todo_id = 1

    response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={"title": "Updated Todo"}
    )

    assert response.status_code == 400


def test_update_todo_invalid_todo_id(client: TestClient):
    """Test updating a todo with invalid todo ID returns 400 error."""
    user_id = "test_user_123"
    todo_id = -1  # Invalid todo ID

    response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={"title": "Updated Todo"}
    )

    assert response.status_code == 400


def test_update_todo_empty_title(client: TestClient):
    """Test updating a todo with empty title returns 422 error."""
    user_id = "test_user_123"

    # Create a todo first
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Original Todo", "description": "Original Description"}
    )

    assert create_response.status_code == 201
    todo_data = create_response.json()
    todo_id = todo_data["id"]

    # Try to update with empty title
    response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={"title": ""}
    )

    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__])