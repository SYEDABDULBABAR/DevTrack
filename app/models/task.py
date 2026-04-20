from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Import only during type checking to avoid circular dependencies
if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.comment import Comment

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="todo")  # todo, in-progress, completed
    priority: str = Field(default="medium")  # low, medium, high
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = Field(default=None)

    # Foreign Key: Link to the Projects table
    project_id: int = Field(foreign_key="projects.id", ondelete="CASCADE")

    # --- Relationships ---
    
    # 'project' indicates which project this task belongs to
    project: Optional["Project"] = Relationship(back_populates="tasks")
    
    # 'comments' retrieves all discussions/comments associated with this task
    # Note: "Comment" is in quotes to prevent circular import errors at runtime
    comments: List["Comment"] = Relationship(back_populates="task", cascade_delete=True)