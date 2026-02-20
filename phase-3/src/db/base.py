from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class BaseSQLModel(SQLModel):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# To be imported by models to inherit common fields
