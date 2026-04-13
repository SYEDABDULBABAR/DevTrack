from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr  # Email format valid karne ke liye

class UserCreate(UserBase):
    password: str  # Registration ke waqt password chahiye

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Token schema (Login ke waqt kaam aayega)
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None