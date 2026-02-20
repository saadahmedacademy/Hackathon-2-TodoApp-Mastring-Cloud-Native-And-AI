from uuid import UUID
import pytest
from sqlmodel import Session, SQLModel, create_engine
from src.db.base import BaseSQLModel
from src.models.conversation import Conversation
from src.repositories.conversation import ConversationRepository

# Use an in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="conversation_repo")
def conversation_repository_fixture(session: Session):
    return ConversationRepository(session)


def test_create_conversation(conversation_repo: ConversationRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    conversation = conversation_repo.create(Conversation(user_id=user_id))

    assert conversation.id is not None
    assert conversation.user_id == user_id
    assert conversation.created_at is not None
    assert conversation.updated_at is not None


def test_get_conversation(conversation_repo: ConversationRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    created_conversation = conversation_repo.create(Conversation(user_id=user_id))

    retrieved_conversation = conversation_repo.get(created_conversation.id)

    assert retrieved_conversation is not None
    assert retrieved_conversation.id == created_conversation.id
    assert retrieved_conversation.user_id == user_id


def test_get_all_conversations(conversation_repo: ConversationRepository):
    user_id_1 = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    user_id_2 = UUID("b1c2d3e4-f5a6-7890-1234-567890abcdef")
    conversation_repo.create(Conversation(user_id=user_id_1))
    conversation_repo.create(Conversation(user_id=user_id_2))

    conversations = conversation_repo.get_all()
    assert len(conversations) == 2


def test_update_conversation(conversation_repo: ConversationRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    conversation = conversation_repo.create(Conversation(user_id=user_id))

    new_user_id = UUID("f1e2d3c4-b5a6-7890-1234-567890abcdef")
    conversation.user_id = new_user_id
    updated_conversation = conversation_repo.update(conversation)

    assert updated_conversation.user_id == new_user_id
    assert updated_conversation.updated_at > conversation.created_at


def test_delete_conversation(conversation_repo: ConversationRepository):
    user_id = UUID("a1b2c3d4-e5f6-7890-1234-567890abcdef")
    conversation = conversation_repo.create(Conversation(user_id=user_id))

    conversation_repo.delete(conversation.id)
    retrieved_conversation = conversation_repo.get(conversation.id)

    assert retrieved_conversation is None
