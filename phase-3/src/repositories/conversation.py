from sqlmodel import Session
from src.repositories.base import BaseRepository
from src.models.conversation import Conversation

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, session: Session):
        super().__init__(Conversation, session)