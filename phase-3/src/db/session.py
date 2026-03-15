from sqlmodel import Session, create_engine
from .base import BaseSQLModel
from src.config import settings
from typing import Generator

# Optimize engine with connection pooling for better performance
if settings.DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,  # Disable SQL echo for performance
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
else:
    engine = create_engine(settings.DATABASE_URL, echo=False)

def create_db_and_tables(engine):
    BaseSQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
