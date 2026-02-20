from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from src.main import app
from src.db.session import get_db, create_db_and_tables
from src.db.base import BaseSQLModel
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.task import Task
from unittest.mock import MagicMock, patch
import json
from typing import Optional, List, Dict, Any

from src.api.v1.endpoints.chat import get_ai_agent as original_get_ai_agent

@pytest.fixture(name="mock_ai_agent_instance")
def mock_ai_agent_instance_fixture():
    mock_agent = MagicMock()
    mock_agent.tool_map = {
        "add_task_tool": MagicMock(),
    }
    mock_agent.get_response = MagicMock()
    mock_agent.call_tool = MagicMock()
    return mock_agent

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
def client_fixture(session: Session, mock_ai_agent_instance: MagicMock):
    def get_session_override():
        yield session

    with patch('src.db.session.get_db', get_session_override):
        app.dependency_overrides[original_get_ai_agent] = lambda: mock_ai_agent_instance
        try:
            with TestClient(app) as client:
                yield client
        finally:
            app.dependency_overrides.clear()


def test_chat_new_conversation(client: TestClient, session: Session, mock_ai_agent_instance: MagicMock):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    test_message = "Hello, AI!"
    ai_response_content = "Hello there!"
    mock_message = MagicMock()
    mock_message.content = ai_response_content
    mock_message.tool_calls = None
    mock_ai_agent_instance.get_response.return_value = mock_message

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": test_message}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "conversation_id" in response_data
    assert "messages" in response_data
    assert len(response_data["messages"]) == 2
    assert response_data["messages"][0]["role"] == "user"
    assert response_data["messages"][0]["content"] == test_message
    assert response_data["messages"][1]["role"] == "assistant"
    assert response_data["messages"][1]["content"] == ai_response_content
    assert response_data["messages"][1]["tool_calls"] is None


def test_chat_existing_conversation(client: TestClient, session: Session, mock_ai_agent_instance: MagicMock):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")

    initial_message_content = "Hello, AI, create a conversation!"
    initial_ai_response_content = "Conversation created."
    mock_message = MagicMock()
    mock_message.content = initial_ai_response_content
    mock_message.tool_calls = None
    mock_ai_agent_instance.get_response.return_value = mock_message

    initial_response = client.post(
        f"/api/{user_id}/chat",
        json={"message": initial_message_content}
    )
    assert initial_response.status_code == 200
    initial_response_data = initial_response.json()
    conversation_id = initial_response_data["conversation_id"]

    test_message = "How are you?"
    ai_response_content = "I am fine, thank you."
    mock_message.content = ai_response_content
    mock_ai_agent_instance.get_response.return_value = mock_message

    response = client.post(
        f"/api/{user_id}/chat",
        json={"conversation_id": conversation_id, "message": test_message}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["conversation_id"] == conversation_id
    assert "messages" in response_data
    # Full history is returned; final assistant message is last
    assert response_data["messages"][-1]["role"] == "assistant"
    assert response_data["messages"][-1]["content"] == ai_response_content


def test_chat_with_tool_call(client: TestClient, session: Session, mock_ai_agent_instance: MagicMock):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    test_message = "Please add a task: Buy groceries"
    tool_name = "add_task_tool"
    tool_arguments = {"description": "Buy groceries"}

    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_abc123"
    mock_tool_call.type = "function"
    mock_tool_call.function.name = tool_name
    mock_tool_call.function.arguments = json.dumps(tool_arguments)

    # First response: agent requests a tool call
    mock_first_response = MagicMock()
    mock_first_response.content = ""
    mock_first_response.tool_calls = [mock_tool_call]

    # Second response: agent confirms after seeing tool result
    mock_second_response = MagicMock()
    mock_second_response.content = "Task 'Buy groceries' has been added!"
    mock_second_response.tool_calls = None

    mock_ai_agent_instance.get_response.side_effect = [mock_first_response, mock_second_response]

    response = client.post(
        f"/api/{user_id}/chat",
        json={"message": test_message}
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "conversation_id" in response_data
    assert "messages" in response_data
    # Full history: user, assistant(tool_call), tool, assistant(final)
    assert len(response_data["messages"]) == 4

    # user message
    assert response_data["messages"][0]["role"] == "user"
    # assistant message with tool_call
    assert response_data["messages"][1]["role"] == "assistant"
    assert response_data["messages"][1]["tool_calls"] is not None
    # tool result
    assert response_data["messages"][2]["role"] == "tool"
    # final assistant confirmation
    assert response_data["messages"][3]["role"] == "assistant"
    assert response_data["messages"][3]["tool_calls"] is None
    assert "groceries" in response_data["messages"][3]["content"].lower()
