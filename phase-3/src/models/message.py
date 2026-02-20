from sqlmodel import Field, Relationship, SQLModel
from src.db.base import BaseSQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class Message(BaseSQLModel, table=True):
    __tablename__ = "messages"

    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    conversation: "Conversation" = Relationship(back_populates="messages")

    sender: str
    content: str
    tool_calls: Optional[str] = None # Store as JSON string
    tool_outputs: Optional[str] = None # Store as JSON string
