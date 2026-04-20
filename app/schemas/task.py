from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    project_id: int  # Project ID is mandatory when creating a task

class TaskOut(TaskBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True