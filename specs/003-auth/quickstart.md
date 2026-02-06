# Quickstart Guide: Authentication System

## Overview
Guide to setting up and using the authentication system with Better Auth and JWT tokens.

## Prerequisites
- Python 3.10+
- FastAPI
- Better Auth
- Neon PostgreSQL database
- Existing Phase-II backend core (002-backend-core)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install better-exceptions python-jose[cryptography] passlib[argon2] fastapi-users[sqlalchemy]
```

### 2. Configure Better Auth
```python
# Configuration for Better Auth integration
import os
from better_auth import Auth, session

auth = Auth(
    secret=os.getenv("AUTH_SECRET_KEY"),
    algorithm="HS256",
    access_token_expire_minutes=15,  # Short-lived access tokens
    refresh_token_expire_days=30,    # Longer-lived refresh tokens
)
```

### 3. Environment Variables
Create/update `.env` file with:
```env
AUTH_SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
PASSWORD_HASH_ALGORITHM=argon2
```

### 4. Integrate with FastAPI
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_jwt_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
```

## Usage Examples

### User Registration
```python
@app.post("/auth/register")
async def register(user_data: UserRegistrationSchema):
    # Register user with Better Auth
    # Hash password using Argon2
    # Return JWT tokens
```

### User Login
```python
@app.post("/auth/login")
async def login(user_credentials: UserLoginSchema):
    # Validate credentials against hashed password
    # Generate and return JWT tokens
```

### Protected Endpoint
```python
@app.get("/api/{user_id}/tasks")
async def get_tasks(user_id: str, current_user: str = Depends(get_current_user)):
    # Verify current_user matches user_id
    # Return user's tasks only
```

## Testing
```bash
# Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123"}'

# Login to get tokens
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePassword123"}'

# Use token to access protected endpoint
curl -X GET http://localhost:8000/api/user-id-here/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Security Best Practices
- Use HTTPS in production
- Rotate AUTH_SECRET_KEY periodically
- Implement rate limiting for auth endpoints
- Log authentication attempts for security monitoring
- Validate JWT tokens properly with proper error handling