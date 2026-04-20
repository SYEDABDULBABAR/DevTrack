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
    
    # Timestamps (To track when the project was created)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign Key: Link to the User table
    owner_id: int = Field(foreign_key="users.id", ondelete="CASCADE")

    # Relationships
    # 'owner' provides details of the user who created the project
    owner: Optional["User"] = Relationship(back_populates="projects")
    
    # 'tasks' provides a list of all tasks associated with this project
    tasks: List["Task"] = Relationship(back_populates="project", cascade_delete=True)

# Schema for handling partial project updates
class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None