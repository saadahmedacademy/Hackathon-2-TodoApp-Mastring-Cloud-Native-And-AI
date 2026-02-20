from uuid import UUID
import pytest
from unittest.mock import MagicMock, patch, call
from sqlmodel import Session
from src.models.conversation import Conversation
from src.models.message import Message
from src.repositories.conversation import ConversationRepository
from src.repositories.message import MessageRepository
from src.agents.base import AIAgentBase
from src.services.conversation_service import ConversationService
import json
from datetime import datetime, timezone


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_conversation_repo(mock_session):
    repo = MagicMock(spec=ConversationRepository)
    repo.session = mock_session
    return repo


@pytest.fixture
def mock_message_repo(mock_session):
    repo = MagicMock(spec=MessageRepository)
    repo.session = mock_session
    return repo


@pytest.fixture
def mock_ai_agent():
    agent = MagicMock(spec=AIAgentBase)
    agent.tool_map = {}
    return agent


@pytest.fixture
def conversation_service(mock_session, mock_ai_agent, mock_conversation_repo, mock_message_repo):
    service = ConversationService(session=mock_session, ai_agent=mock_ai_agent)
    service.conversation_repo = mock_conversation_repo
    service.message_repo = mock_message_repo
    return service


def test_create_conversation(conversation_service: ConversationService, mock_conversation_repo: MagicMock):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    mock_conversation_repo.create.return_value = Conversation(
        id=UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0"), user_id=user_id
    )

    conversation = conversation_service.create_conversation(user_id)

    mock_conversation_repo.create.assert_called_once()
    called_conversation = mock_conversation_repo.create.call_args.args[0]
    assert called_conversation.user_id == user_id
    assert conversation.user_id == user_id


def test_get_conversation(conversation_service: ConversationService, mock_conversation_repo: MagicMock):
    conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")
    mock_conversation_repo.get.return_value = Conversation(
        id=conv_id, user_id=UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    )

    conversation = conversation_service.get_conversation(conv_id)

    mock_conversation_repo.get.assert_called_once_with(conv_id)
    assert conversation.id == conv_id


def test_add_message_to_conversation(conversation_service: ConversationService, mock_message_repo: MagicMock):
    conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")
    mock_message_repo.create.return_value = Message(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        conversation_id=conv_id,
        sender="user",
        content="Test",
    )

    message = conversation_service.add_message_to_conversation(conv_id, "user", "Test")

    mock_message_repo.create.assert_called_once()
    assert message.content == "Test"


@patch('src.services.conversation_service.ConversationService.get_conversation_history')
def test_send_message_to_agent_new_conversation(
    mock_get_history, conversation_service: ConversationService,
    mock_conversation_repo: MagicMock, mock_message_repo: MagicMock, mock_ai_agent: MagicMock
):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    new_conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")

    mock_conversation_repo.create.return_value = Conversation(id=new_conv_id, user_id=user_id)
    mock_message_repo.create.return_value = Message(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        conversation_id=new_conv_id,
        sender="user",
        content="Hi",
    )

    user_msg = Message(
        conversation_id=new_conv_id,
        sender="user",
        content="Hi",
        created_at=datetime(2026, 1, 1, 0, 0, 0),
    )
    assistant_msg = Message(
        conversation_id=new_conv_id,
        sender="assistant",
        content="Hello!",
        created_at=datetime(2026, 1, 1, 0, 0, 1),
    )

    # First call (after user msg persisted) returns [user_msg]
    # Second call (full history at end) returns [user_msg, assistant_msg]
    mock_get_history.side_effect = [
        [user_msg],          # _is_duplicate_message check
        [user_msg],          # _build_ai_messages
        [user_msg, assistant_msg],  # final full history
    ]

    mock_agent_response = MagicMock()
    mock_agent_response.content = "Hello!"
    mock_agent_response.tool_calls = None
    mock_ai_agent.get_response.return_value = mock_agent_response

    response = conversation_service.send_message_to_agent(user_id, None, "Hi")

    mock_conversation_repo.create.assert_called_once()
    assert response["conversation_id"] == str(new_conv_id)
    # Full history is returned
    assert len(response["messages"]) == 2
    assert response["messages"][0]["role"] == "user"
    assert response["messages"][0]["content"] == "Hi"
    assert response["messages"][1]["role"] == "assistant"
    assert response["messages"][1]["content"] == "Hello!"


@patch('src.services.conversation_service.ConversationService.get_conversation_history')
def test_send_message_to_agent_existing_conversation(
    mock_get_history, conversation_service: ConversationService,
    mock_conversation_repo: MagicMock, mock_message_repo: MagicMock, mock_ai_agent: MagicMock
):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    existing_conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")

    mock_conversation_repo.get.return_value = Conversation(id=existing_conv_id, user_id=user_id)
    mock_message_repo.create.return_value = Message(
        conversation_id=existing_conv_id, sender="user", content="How are you?"
    )

    prior_msg = Message(
        conversation_id=existing_conv_id,
        sender="user",
        content="Hi",
        created_at=datetime(2026, 1, 1, 0, 0, 0),
    )
    new_user_msg = Message(
        conversation_id=existing_conv_id,
        sender="user",
        content="How are you?",
        created_at=datetime(2026, 1, 1, 0, 0, 1),
    )
    assistant_msg = Message(
        conversation_id=existing_conv_id,
        sender="assistant",
        content="I am good!",
        created_at=datetime(2026, 1, 1, 0, 0, 2),
    )

    mock_get_history.side_effect = [
        [prior_msg],                                     # dedup check
        [prior_msg, new_user_msg],                       # _build_ai_messages
        [prior_msg, new_user_msg, assistant_msg],        # final history
    ]

    mock_agent_response = MagicMock()
    mock_agent_response.content = "I am good!"
    mock_agent_response.tool_calls = None
    mock_ai_agent.get_response.return_value = mock_agent_response

    response = conversation_service.send_message_to_agent(user_id, existing_conv_id, "How are you?")

    mock_conversation_repo.get.assert_called_once_with(existing_conv_id)
    assert response["conversation_id"] == str(existing_conv_id)
    assert response["messages"][-1]["role"] == "assistant"
    assert response["messages"][-1]["content"] == "I am good!"


@patch('src.services.conversation_service.ConversationService.get_conversation_history')
def test_send_message_to_agent_with_tool_call(
    mock_get_history, conversation_service: ConversationService,
    mock_conversation_repo: MagicMock, mock_message_repo: MagicMock, mock_ai_agent: MagicMock
):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")

    mock_conversation_repo.create.return_value = Conversation(id=conv_id, user_id=user_id)
    mock_message_repo.create.return_value = Message(
        conversation_id=conv_id, sender="user", content="Create a task"
    )

    user_msg = Message(
        conversation_id=conv_id,
        sender="user",
        content="Create a task",
        created_at=datetime(2026, 1, 1, 0, 0, 0),
    )
    assistant_tool_msg = Message(
        conversation_id=conv_id,
        sender="assistant",
        content="",
        tool_calls=json.dumps([{
            "id": "call_abc123", "type": "function",
            "function": {"name": "add_task_tool", "arguments": json.dumps({"description": "Buy milk"})},
        }]),
        created_at=datetime(2026, 1, 1, 0, 0, 1),
    )
    tool_result_msg = Message(
        conversation_id=conv_id,
        sender="tool",
        content=json.dumps({"status": "success", "task_id": "abc", "message": "Task created."}),
        tool_outputs=json.dumps({
            "tool_call_id": "call_abc123",
            "name": "add_task_tool",
            "output": {"status": "success", "task_id": "abc", "message": "Task created."},
        }),
        created_at=datetime(2026, 1, 1, 0, 0, 2),
    )
    final_assistant_msg = Message(
        conversation_id=conv_id,
        sender="assistant",
        content="Task 'Buy milk' was created!",
        created_at=datetime(2026, 1, 1, 0, 0, 3),
    )

    # Build a proper tool call mock
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_abc123"
    mock_tool_call.type = "function"
    mock_tool_call.function.name = "add_task_tool"
    mock_tool_call.function.arguments = json.dumps({"description": "Buy milk"})

    # First agent call returns tool call, second returns final text
    mock_first_response = MagicMock()
    mock_first_response.content = ""
    mock_first_response.tool_calls = [mock_tool_call]

    mock_second_response = MagicMock()
    mock_second_response.content = "Task 'Buy milk' was created!"
    mock_second_response.tool_calls = None

    mock_ai_agent.get_response.side_effect = [mock_first_response, mock_second_response]

    # get_conversation_history call sequence:
    # 1. dedup check → []
    # 2. _build_ai_messages → [user_msg]
    # 3. final full history
    mock_get_history.side_effect = [
        [],                # dedup check (new conversation)
        [user_msg],        # _build_ai_messages
        [user_msg, assistant_tool_msg, tool_result_msg, final_assistant_msg],  # final history
    ]

    fake_tool_output = {"status": "success", "task_id": "abc", "message": "Task created."}
    mock_dispatch = MagicMock(return_value=fake_tool_output)
    conversation_service._tool_dispatch["add_task_tool"] = mock_dispatch

    response = conversation_service.send_message_to_agent(user_id, None, "Create a task")

    mock_dispatch.assert_called_once_with(user_id, description="Buy milk")
    assert response["conversation_id"] == str(conv_id)
    # Full history: user, assistant(tool_call), tool, assistant(final)
    assert len(response["messages"]) == 4
    assert response["messages"][0]["role"] == "user"
    assert response["messages"][1]["role"] == "assistant"
    assert response["messages"][2]["role"] == "tool"
    assert response["messages"][3]["role"] == "assistant"
    assert response["messages"][3]["content"] == "Task 'Buy milk' was created!"


@patch('src.services.conversation_service.ConversationService.get_conversation_history')
def test_duplicate_message_not_inserted(
    mock_get_history, conversation_service: ConversationService,
    mock_conversation_repo: MagicMock, mock_message_repo: MagicMock, mock_ai_agent: MagicMock
):
    """If the last message is identical and recent, it must not be re-inserted."""
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    existing_conv_id = UUID("c1c2c3c4-e5f6-7890-1234-567890abcde0")

    mock_conversation_repo.get.return_value = Conversation(id=existing_conv_id, user_id=user_id)

    recent_msg = Message(
        conversation_id=existing_conv_id,
        sender="user",
        content="Hello AI!",
        created_at=datetime.now(timezone.utc),  # very recent
    )
    assistant_msg = Message(
        conversation_id=existing_conv_id,
        sender="assistant",
        content="Hi there!",
        created_at=datetime.now(timezone.utc),
    )

    mock_get_history.side_effect = [
        [recent_msg],                        # dedup check — duplicate found
        [recent_msg],                        # _build_ai_messages
        [recent_msg, assistant_msg],         # final history
    ]

    mock_agent_response = MagicMock()
    mock_agent_response.content = "Hi there!"
    mock_agent_response.tool_calls = None
    mock_ai_agent.get_response.return_value = mock_agent_response

    response = conversation_service.send_message_to_agent(user_id, existing_conv_id, "Hello AI!")

    # message_repo.create should NOT have been called for the user message
    # (it may still be called for the assistant message)
    create_calls = mock_message_repo.create.call_args_list
    user_inserts = [c for c in create_calls if c.args[0].sender == "user"]
    assert len(user_inserts) == 0, "Duplicate user message must not be inserted"
