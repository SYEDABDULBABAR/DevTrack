from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

# 1. Create the database engine (Retrieves URL directly from settings)
# Setting echo=True will print all generated SQL queries to the terminal for debugging
engine = create_engine(
    settings.DATABASE_URL, 
    echo=True
)

# 2. Dependency function to provide a database session to routes
def get_session():
    with Session(engine) as session:
        yield session

# 3. Function to initialize the database and create all defined tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)