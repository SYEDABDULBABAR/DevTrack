from fastapi import FastAPI
from app.db.database import engine
from sqlmodel import SQLModel
from app.routers import auth, users, projects, tasks, comments # <-- 'comments' add kiya
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.comment import Comment

app = FastAPI(title="DevTrack API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Routers register karein
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(comments.router) # <-- Ye line lazmi add karein