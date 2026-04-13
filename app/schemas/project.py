from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass  # User se input lete waqt

class ProjectOut(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True