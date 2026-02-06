"""Comprehensive integration tests for the full todo workflow."""
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


def test_full_todo_workflow(client: TestClient):
    """Test the complete workflow of todo operations."""
    user_id = "test_user_workflow"

    # Step 1: Create a todo
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={
            "title": "Workflow Test Todo",
            "description": "This todo will go through the full workflow"
        }
    )
    assert create_response.status_code == 201
    created_todo = create_response.json()
    assert created_todo["title"] == "Workflow Test Todo"
    assert created_todo["description"] == "This todo will go through the full workflow"
    assert created_todo["completed"] is False
    todo_id = created_todo["id"]

    # Step 2: Retrieve the created todo
    get_single_response = client.get(f"/api/{user_id}/tasks/{todo_id}")
    assert get_single_response.status_code == 200
    retrieved_todo = get_single_response.json()
    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["title"] == "Workflow Test Todo"

    # Step 3: Get all todos for the user
    get_all_response = client.get(f"/api/{user_id}/tasks")
    assert get_all_response.status_code == 200
    all_todos = get_all_response.json()
    assert len(all_todos) == 1
    assert all_todos[0]["id"] == todo_id

    # Step 4: Update the todo
    update_response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={
            "title": "Updated Workflow Test Todo",
            "description": "This todo has been updated",
            "completed": True
        }
    )
    assert update_response.status_code == 200
    updated_todo = update_response.json()
    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Updated Workflow Test Todo"
    assert updated_todo["completed"] is True

    # Step 5: Mark as incomplete again
    mark_incomplete_response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": False}
    )
    assert mark_incomplete_response.status_code == 200
    marked_todo = mark_incomplete_response.json()
    assert marked_todo["id"] == todo_id
    assert marked_todo["completed"] is False

    # Step 6: Mark as complete again
    mark_complete_response = client.patch(
        f"/api/{user_id}/tasks/{todo_id}/complete",
        params={"completed": True}
    )
    assert mark_complete_response.status_code == 200
    completed_todo = mark_complete_response.json()
    assert completed_todo["id"] == todo_id
    assert completed_todo["completed"] is True

    # Step 7: Delete the todo
    delete_response = client.delete(f"/api/{user_id}/tasks/{todo_id}")
    assert delete_response.status_code == 204

    # Step 8: Verify the todo is deleted
    verify_deleted_response = client.get(f"/api/{user_id}/tasks/{todo_id}")
    assert verify_deleted_response.status_code == 404


def test_multiple_users_isolation(client: TestClient):
    """Test that different users have isolated todo lists."""
    user1_id = "user_1_isolated"
    user2_id = "user_2_isolated"

    # Create a todo for user 1
    user1_create_response = client.post(
        f"/api/{user1_id}/tasks",
        json={"title": "User 1 Todo", "description": "Owned by user 1"}
    )
    assert user1_create_response.status_code == 201
    user1_todo = user1_create_response.json()
    user1_todo_id = user1_todo["id"]

    # Create a todo for user 2
    user2_create_response = client.post(
        f"/api/{user2_id}/tasks",
        json={"title": "User 2 Todo", "description": "Owned by user 2"}
    )
    assert user2_create_response.status_code == 201
    user2_todo = user2_create_response.json()
    user2_todo_id = user2_todo["id"]

    # Verify user 1 can only see their own todo
    user1_get_all_response = client.get(f"/api/{user1_id}/tasks")
    assert user1_get_all_response.status_code == 200
    user1_todos = user1_get_all_response.json()
    assert len(user1_todos) == 1
    assert user1_todos[0]["id"] == user1_todo_id

    # Verify user 2 can only see their own todo
    user2_get_all_response = client.get(f"/api/{user2_id}/tasks")
    assert user2_get_all_response.status_code == 200
    user2_todos = user2_get_all_response.json()
    assert len(user2_todos) == 1
    assert user2_todos[0]["id"] == user2_todo_id

    # Verify users cannot access each other's todos
    user1_access_user2_response = client.get(f"/api/{user1_id}/tasks/{user2_todo_id}")
    assert user1_access_user2_response.status_code == 404  # Not found for this user

    user2_access_user1_response = client.get(f"/api/{user2_id}/tasks/{user1_todo_id}")
    assert user2_access_user1_response.status_code == 404  # Not found for this user


def test_validation_errors(client: TestClient):
    """Test various validation error scenarios."""
    user_id = "test_user_validation"

    # Test creating a todo with empty title
    empty_title_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "", "description": "This should fail"}
    )
    assert empty_title_response.status_code == 422

    # Test creating a todo with very long title
    long_title_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "A" * 256, "description": "This should fail due to long title"}
    )
    assert long_title_response.status_code == 422

    # Test updating with empty title
    create_response = client.post(
        f"/api/{user_id}/tasks",
        json={"title": "Valid Todo", "description": "Initially valid"}
    )
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    update_empty_title_response = client.put(
        f"/api/{user_id}/tasks/{todo_id}",
        json={"title": ""}
    )
    assert update_empty_title_response.status_code == 422

    # Test accessing with invalid user ID
    invalid_user_response = client.get(f"/api//tasks")  # Empty user ID
    assert invalid_user_response.status_code == 400


if __name__ == "__main__":
    pytest.main([__file__])