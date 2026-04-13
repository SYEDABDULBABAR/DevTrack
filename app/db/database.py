from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# 1. Engine create karein (Directly settings se URL uthayega)
# echo=True ka matlab hai ke terminal mein SQL queries print hongi
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True
)

# 2. Dependency function jo database session provide karega
def get_session():
    with Session(engine) as session:
        yield session

# 3. Database tables create karne ke liye function
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)