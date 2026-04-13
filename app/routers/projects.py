from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from app.db.database import get_session
from app.models.project import Project
from app.models.user import User
from app.core.security import get_current_user
from typing import List, Optional

# Schema for creating a project (taake user se sirf zaroori data lein)
class ProjectCreate(SQLModel):
    title: str
    description: Optional[str] = None

router = APIRouter(prefix="/projects", tags=["Projects"])

# 1. POST: Create Project
@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    # Data ko Project model mein convert karein aur owner_id set karein
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        owner_id=current_user.id
    )
    
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project

# 2. GET: Read All Projects (Sirf current user ke)
@router.get("/", response_model=List[Project])
def read_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Sirf wahi projects dikhayega jo is user ke hain
    statement = select(Project).where(Project.owner_id == current_user.id)
    projects = session.exec(statement).all()
    return projects

# 3. GET: Read Single Project (by ID)
@router.get("/{project_id}", response_model=Project)
def read_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project nahi mila")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Aapko is project ki permission nahi hai")
        
    return project