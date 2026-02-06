"""Test fixtures for authentication testing."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.db.session import get_session


@pytest.fixture(name="engine")
def fixture_engine():
    """Create an in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(name="session")
def fixture_session(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(session):
    """Create a test client with overridden dependencies."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="sample_user_data")
def fixture_sample_user_data():
    """Sample user registration data for testing."""
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "name": "Test User"
    }


@pytest.fixture(name="sample_login_data")
def fixture_sample_login_data():
    """Sample user login data for testing."""
    return {
        "email": "test@example.com",
        "password": "securepassword123"
    }