"""Authentication configuration settings."""

from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
JWT_SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_key_for_development")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

# Password hashing configuration
PASSWORD_HASH_SCHEME = "argon2"

# Token expiration settings
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DELTA = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)