"""Database engine configuration for the todo application."""
from sqlmodel import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# Create the database engine with appropriate settings for production
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "False").lower() == "true",  # Enable SQL logging in debug mode
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)