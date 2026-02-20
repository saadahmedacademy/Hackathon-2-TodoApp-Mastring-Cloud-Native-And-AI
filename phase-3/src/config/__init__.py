import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    MCP_SDK_CLIENT_ID: Optional[str] = None
    MCP_SDK_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file_encoding = 'utf-8'

# Construct the absolute path to the .env file in the phase-3 directory
# This assumes .env is directly in the phase-3 directory, and pytest is run from the project root.
_current_dir = os.path.dirname(os.path.abspath(__file__)) # This is src/config/
_phase3_root = os.path.abspath(os.path.join(_current_dir, '..', '..')) # This is /home/saadahmed/hk-2-project/phase-3/
_env_file_path = os.path.join(_phase3_root, '.env') # This is /home/saadahmed/hk-2-project/phase-3/.env

settings = Settings(_env_file=_env_file_path) # Pass env_file explicitly