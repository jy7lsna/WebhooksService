import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from environment or config
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create SQLAlchemy engine
# For SQLite, need connect_args; for PostgreSQL, remove connect_args
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session (for FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Optional: Function to initialize tables (if needed)
def init_db():
    Base.metadata.create_all(bind=engine)
