from sqlmodel import Field, Relationship, SQLModel
from src.db.base import BaseSQLModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from src.models.message import Message # Import Message

class Conversation(BaseSQLModel, table=True):
    __tablename__ = "conversations"

    user_id: UUID = Field(index=True)

    messages: List[Message] = Relationship(back_populates="conversation")
