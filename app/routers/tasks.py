from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from app.db.database import get_session
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.core.security import get_current_user
from typing import List, Optional

# --- SCHEMAS ---

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    project_id: int
    priority: Optional[str] = "medium"
    status: Optional[str] = "To Do"

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# --- ENDPOINTS ---

# 1. POST: Create Task
@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    # Verify project existence and ownership
    project = session.get(Project, task_data.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You do not have permission to create tasks in this project"
        )

    new_task = Task(**task_data.model_dump())
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

# 2. GET: Read Tasks (With Filter Support)
@router.get("/", response_model=List[Task])
def get_tasks(
    status: Optional[str] = None, # Query parameter: ?status=Done
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Join logic to ensure only tasks belonging to the user's projects are returned
    statement = select(Task).join(Project).where(Project.owner_id == current_user.id)
    
    if status:
        statement = statement.where(Task.status == status)
        
    tasks = session.exec(statement).all()
    return tasks

# 3. PATCH: Quick Complete Task
@router.patch("/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    project = session.get(Project, task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")

    task.status = "Done"
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# 4. PUT: Update Full Task Data
@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    project = session.get(Project, db_task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# 5. DELETE: Remove Task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    project = session.get(Project, db_task.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this task")

    session.delete(db_task)
    session.commit()
    return {"message": "Task successfully deleted"}