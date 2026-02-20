from sqlmodel import Session, create_engine
from .base import BaseSQLModel
from src.config import settings
from typing import Generator

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables(engine):
    BaseSQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
