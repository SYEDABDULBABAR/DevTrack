from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task

class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    
    # Timestamps (Record rakhne ke liye ke project kab bana)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign Key: User table se link
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE")

    # Relationships
    # 'owner' project banane wale user ki details dega
    owner: Optional["User"] = Relationship(back_populates="projects")
    
    # 'tasks' is project ke andar maujood tamam tasks ki list dega
    tasks: List["Task"] = Relationship(back_populates="project", cascade_delete=True)