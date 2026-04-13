from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

# Circular import se bachne ke liye TYPE_CHECKING ka use
if TYPE_CHECKING:
    from app.models.project import Project

# 1. Base Model (Jo Create aur Update mein kaam aata hai)
class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)

# 2. Database Model (Jo Table banyega)
class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    
    # Relationships
    # Ek user ke boht saare projects ho sakte hain
    projects: List["Project"] = Relationship(back_populates="owner")