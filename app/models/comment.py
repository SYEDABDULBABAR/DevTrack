from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

# Circular import se bachne ke liye
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Keys
    # Task link: Kis task par comment kiya gaya
    task_id: int = Field(foreign_key="tasks.id", ondelete="CASCADE")
    
    # User link: Kis ne comment kiya (Auth user tracking)
    user_id: int = Field(foreign_key="users.id")

    # --- Relationships ---
    
    # 'task' link wapis Task model se
    task: Optional["Task"] = Relationship(back_populates="comments")
    
    # 'author' link User model se 
    author: Optional["User"] = Relationship()

# Yeh extra class API input handle karne ke liye hai
class CommentCreate(SQLModel):
    content: str
    task_id: int