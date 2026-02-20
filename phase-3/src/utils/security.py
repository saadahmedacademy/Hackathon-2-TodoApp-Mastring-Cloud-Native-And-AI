from uuid import UUID
from fastapi import HTTPException, status

def validate_user_id(user_id: UUID):
    """
    Validates if a given user_id is a valid UUID.
    In a more complex system, this might involve checking against a user service
    to ensure the user actually exists.
    """
    if not isinstance(user_id, UUID):
        try:
            UUID(str(user_id))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid user_id format: {user_id}. Must be a valid UUID."
            )
    return user_id