from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

# Use TYPE_CHECKING to avoid circular imports during static analysis
if TYPE_CHECKING:
    from app.models.project import Project

# 1. Base Model (Common fields used for Creation and Updates)
class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)

# 2. Database Model (Maps directly to the database table)
class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    
    # Relationships
    # One-to-Many: A single user can be the owner of multiple projects
    projects: List["Project"] = Relationship(back_populates="owner")