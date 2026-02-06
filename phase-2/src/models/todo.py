"""SQLModel models for the todo application."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TodoBase(SQLModel):
    """Base model containing common fields for Todo."""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    """SQLModel for Todo entity with database table configuration."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Foreign key to user, indexed for performance
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoRead(TodoBase):
    """Schema for reading Todo data."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TodoCreate(TodoBase):
    """Schema for creating new Todo items."""
    title: str = Field(min_length=1, max_length=255)  # Required field
    pass  # Inherits other fields from TodoBase


class TodoUpdate(SQLModel):
    """Schema for updating Todo items."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None