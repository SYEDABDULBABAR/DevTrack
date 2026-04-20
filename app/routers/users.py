from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User, UserBase
from typing import Any

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserBase)
def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """
    Protected route: Returns the profile information of the currently authenticated user.
    Using response_model=UserBase ensures that the sensitive hashed_password is excluded.
    """
    return current_user