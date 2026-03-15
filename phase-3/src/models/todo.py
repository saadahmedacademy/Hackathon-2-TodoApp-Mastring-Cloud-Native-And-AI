"""
Phase-3 Todo model — maps to the shared 'todo' table owned by Phase-2.

Schema must remain 100% compatible with Phase-2's phase-2/src/models/todo.py.
The ONLY Phase-3 addition is `display_id`: a per-user sequential integer.

FIELD RULES (must match Phase-2 exactly):
  title:       min_length=1, max_length=255  (matches Phase-2 Field constraints)
  description: max_length=1000, optional
  completed:   bool, default=False
  user_id:     str  (UUID stored as str — Phase-2 convention)
  created_at:  datetime
  updated_at:  datetime
"""

from sqlmodel import SQLModel, Field, Index
from datetime import datetime
from typing import Optional


class Todo(SQLModel, table=True):
    """Shared todo table — Phase-3 read/write, Phase-2 canonical owner."""

    __tablename__ = "todo"
    __table_args__ = (
        # Composite indexes for optimized queries
        Index("ix_todo_user_display", "user_id", "display_id"),
        Index("ix_todo_user_completed", "user_id", "completed"),
    )

    # ── Phase-2 compatible fields (must not diverge) ────────────────────────
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)               # UUID stored as str
    title: str = Field(min_length=1, max_length=255)  # matches Phase-2 constraint
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # ── Phase-3 extension — per-user sequential display ID ──────────────────
    # Backfilled via Alembic migration a1b2c3d4e5f6.
    # Phase-2 does NOT know about this column (it's invisible to Phase-2 ORM).
    display_id: Optional[int] = Field(default=None, index=True)
