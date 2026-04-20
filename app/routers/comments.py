from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.comment import Comment, CommentCreate
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.core.security import get_current_user
from typing import List

router = APIRouter(prefix="/comments", tags=["Comments"])

# 1. POST: Add a Comment to a Task
@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if the task exists
    task = session.get(Task, comment_data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Access check: Only the project owner is allowed to add comments
    project = session.get(Project, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to comment on this task")

    new_comment = Comment(
        content=comment_data.content,
        task_id=comment_data.task_id,
        user_id=current_user.id
    )
    
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

# 2. GET: List all comments for a specific task
@router.get("/{task_id}", response_model=List[Comment])
def get_task_comments(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if the task exists
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Access check: Only the project owner can view comments
    project = session.get(Project, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    statement = select(Comment).where(Comment.task_id == task_id)
    comments = session.exec(statement).all()
    return comments