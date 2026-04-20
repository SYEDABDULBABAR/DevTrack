from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

# Used to prevent circular imports during type checking
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Keys
    # Task link: Identifies which task this comment belongs to
    task_id: int = Field(foreign_key="tasks.id", ondelete="CASCADE")
    
    # User link: Identifies the author of the comment (Authenticated user tracking)
    user_id: int = Field(foreign_key="users.id")

    # --- Relationships ---
    
    # Links back to the Task model
    task: Optional["Task"] = Relationship(back_populates="comments")
    
    # Links to the User model to identify the author
    author: Optional["User"] = Relationship()

# Schema for handling API input during comment creation
class CommentCreate(SQLModel):
    content: str
    task_id: int