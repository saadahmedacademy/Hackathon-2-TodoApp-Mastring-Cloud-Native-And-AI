from uuid import UUID
import pytest
from sqlmodel import Session, SQLModel, create_engine
from src.db.base import BaseSQLModel
from src.models.task import Task
from src.repositories.task_repository import TaskRepository

# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine) # Create tables for Task model as well
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="task_repo")
def task_repository_fixture(session: Session):
    return TaskRepository(session)


def test_create_task(task_repo: TaskRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    task = task_repo.create(Task(user_id=user_id, description="Buy groceries"))

    assert task.id is not None
    assert task.user_id == user_id
    assert task.description == "Buy groceries"
    assert task.status == "pending"
    assert task.created_at is not None
    assert task.updated_at is not None


def test_get_task(task_repo: TaskRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    created_task = task_repo.create(Task(user_id=user_id, description="Read book"))

    retrieved_task = task_repo.get(created_task.id)

    assert retrieved_task is not None
    assert retrieved_task.id == created_task.id
    assert retrieved_task.description == "Read book"


def test_get_all_tasks(task_repo: TaskRepository):
    user_id_1 = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    user_id_2 = UUID("b1c2d3e4-f5a6-7890-1234-567890abcdef")
    task_repo.create(Task(user_id=user_id_1, description="Task 1"))
    task_repo.create(Task(user_id=user_id_2, description="Task 2"))

    tasks = task_repo.get_all()
    assert len(tasks) == 2


def test_update_task(task_repo: TaskRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    task = task_repo.create(Task(user_id=user_id, description="Old description", status="pending"))

    task.description = "New description"
    task.status = "completed"
    updated_task = task_repo.update(task)

    assert updated_task.description == "New description"
    assert updated_task.status == "completed"
    assert updated_task.updated_at > task.created_at


def test_delete_task(task_repo: TaskRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    task = task_repo.create(Task(user_id=user_id, description="To be deleted"))

    task_repo.delete(task.id)
    retrieved_task = task_repo.get(task.id)

    assert retrieved_task is None
