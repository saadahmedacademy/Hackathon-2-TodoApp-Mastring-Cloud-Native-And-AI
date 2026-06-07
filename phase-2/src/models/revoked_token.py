from sqlmodel import SQLModel, Field

from datetime import datetime

import uuid


class RevokedToken(SQLModel, table=True):

    """Stores invalidated refresh tokens after logout."""

    __tablename__ = "revoked_tokens"


    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    token_jti: str = Field(unique=True, index=True, nullable=False)

    revoked_at: datetime = Field(default_factory=datetime.utcnow)

    expires_at: datetime = Field(nullable=False)
