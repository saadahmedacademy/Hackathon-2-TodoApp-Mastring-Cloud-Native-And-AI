from sqlmodel import Session
from src.repositories.base import BaseRepository
from src.models.message import Message

class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: Session):
        super().__init__(Message, session)