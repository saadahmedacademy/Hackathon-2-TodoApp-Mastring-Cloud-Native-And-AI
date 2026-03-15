"""Database session management for the todo application."""
from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Optimize engine with connection pooling for PostgreSQL
# These settings improve performance under concurrent load
connect_args = {}
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL-specific optimizations
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Disable SQL echo in production for performance
        pool_size=10,  # Number of connections to keep in pool
        max_overflow=20,  # Max additional connections beyond pool_size
        pool_pre_ping=True,  # Verify connections before using them
        pool_recycle=3600,  # Recycle connections after 1 hour
    )
else:
    # SQLite or other databases
    engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session