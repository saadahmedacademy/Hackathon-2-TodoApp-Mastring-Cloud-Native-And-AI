from uuid import UUID
import pytest
from sqlmodel import Session, SQLModel, create_engine
from src.db.base import BaseSQLModel
from src.models.conversation import Conversation
from src.models.message import Message
from src.repositories.conversation import ConversationRepository
from src.repositories.message import MessageRepository

# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="conversation")
def conversation_fixture(session: Session):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    repo = ConversationRepository(session)
    return repo.create(Conversation(user_id=user_id))


@pytest.fixture(name="message_repo")
def message_repository_fixture(session: Session):
    return MessageRepository(session)


def test_create_message(message_repo: MessageRepository, conversation: Conversation):
    message = message_repo.create(
        Message(conversation_id=conversation.id, sender="user", content="Hello AI!")
    )

    assert message.id is not None
    assert message.conversation_id == conversation.id
    assert message.sender == "user"
    assert message.content == "Hello AI!"
    assert message.created_at is not None
    assert message.updated_at is not None


def test_get_message(message_repo: MessageRepository, conversation: Conversation):
    created_message = message_repo.create(
        Message(conversation_id=conversation.id, sender="user", content="Test message")
    )

    retrieved_message = message_repo.get(created_message.id)

    assert retrieved_message is not None
    assert retrieved_message.id == created_message.id
    assert retrieved_message.content == "Test message"


def test_get_all_messages(message_repo: MessageRepository, conversation: Conversation):
    message_repo.create(
        Message(conversation_id=conversation.id, sender="user", content="Message 1")
    )
    message_repo.create(
        Message(conversation_id=conversation.id, sender="assistant", content="Response 1")
    )

    messages = message_repo.get_all()
    assert len(messages) == 2


def test_update_message(message_repo: MessageRepository, conversation: Conversation):
    message = message_repo.create(
        Message(conversation_id=conversation.id, sender="user", content="Initial content")
    )

    message.content = "Updated content"
    updated_message = message_repo.update(message)

    assert updated_message.content == "Updated content"
    assert updated_message.updated_at > message.created_at


def test_delete_message(message_repo: MessageRepository, conversation: Conversation):
    message = message_repo.create(
        Message(conversation_id=conversation.id, sender="user", content="To be deleted")
    )

    message_repo.delete(message.id)
    retrieved_message = message_repo.get(message.id)

    assert retrieved_message is None
