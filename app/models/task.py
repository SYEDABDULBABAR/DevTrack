from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Circular imports se bachne ke liye sirf type checking ke waqt import karein
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

    # Foreign Key: Project table se link (Make sure your project table name is "projects")
    project_id: int = Field(foreign_key="projects.id", ondelete="CASCADE")

    # --- Relationships ---
    
    # 'project' humein batayega ke ye task kis project ka hissa hai
    project: Optional["Project"] = Relationship(back_populates="tasks")
    
    # 'comments' is task par hone wali saari baatein
    # "Comment" ko quotes mein rakha hai taake circular import error na aaye
    comments: List["Comment"] = Relationship(back_populates="task", cascade_delete=True)