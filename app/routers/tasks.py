from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from app.db.database import get_session
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.core.security import get_current_user
from typing import List, Optional

# Schema: Task create karte waqt user se kya lena hai
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    project_id: int
    priority: Optional[str] = "medium"

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# 1. POST: Naya Task banayein
@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    # Check karein ke jis project mein task dal raha hai, wo isi user ka hai?
    project = session.get(Project, task_data.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Aap is project mein task nahi bana sakte")

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        priority=task_data.priority
    )
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

# 2. GET: Saare Tasks dekhne ke liye (Security ke saath)
@router.get("/", response_model=List[Task])
def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Sirf wahi tasks jo is user ke projects se link hain
    statement = select(Task).join(Project).where(Project.owner_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks

# 3. PATCH: Task ko complete mark karne ke liye
@router.patch("/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task nahi mila")
    
    # Check permission
    project = session.get(Project, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    task.status = "completed"
    session.add(task)
    session.commit()
    session.refresh(task)
    return task