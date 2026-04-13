from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.models.user import User, UserBase
from typing import Any

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserBase)
def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """
    Protected route: Yeh login shuda user ki profile info return karega.
    response_model=UserBase lagane se hashed_password hide ho jayega.
    """
    return current_user