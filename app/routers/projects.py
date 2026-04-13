from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, SQLModel
from app.db.database import get_session
from app.models.project import Project
from app.models.user import User
from app.core.security import get_current_user
from typing import List, Optional

# --- SCHEMAS ---

# Project create karne ke liye
class ProjectCreate(SQLModel):
    title: str
    description: Optional[str] = None

# Project update karne ke liye (Sirf title aur description allow hai)
class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None

router = APIRouter(prefix="/projects", tags=["Projects"])

# --- ENDPOINTS ---

# 1. POST: Create Project
@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate, 
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        owner_id=current_user.id
    )
    
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    return new_project

# 2. GET: Read All Projects (Sirf wahi jo login user ke hain)
@router.get("/", response_model=List[Project])
def read_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
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
        raise HTTPException(status_code=403, detail="Aapko is project ko dekhne ki permission nahi hai")
        
    return project

# 4. PUT: Update Project (Owner Only)
@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int, 
    project_data: ProjectUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project nahi mila")
    
    # Check if login user is the owner
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Aap sirf apna project update kar sakte hain")

    # Update only the fields that were provided
    update_data = project_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

# 5. DELETE: Delete Project (Owner Only)
@router.delete("/{project_id}")
def delete_project(
    project_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project nahi mila")

    # Check if login user is the owner
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Aap sirf apna project delete kar sakte hain")

    session.delete(db_project)
    session.commit()
    return {"message": f"Project '{db_project.title}' delete ho gaya hai"}