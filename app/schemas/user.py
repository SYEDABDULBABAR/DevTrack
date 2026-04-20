from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr  # Used to validate the email format

class UserCreate(UserBase):
    password: str  # Required field during user registration

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Token schema (Used for authentication responses)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None