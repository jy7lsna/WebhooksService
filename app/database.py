<<<<<<< HEAD
import os
from dotenv import load_dotenv
=======
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

DATABASE_URL = "sqlite:///./test.db"  # Use PostgreSQL if you prefer

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
>>>>>>> 65cd0d2 (Initial Commit)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

<<<<<<< HEAD
load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session
=======
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

>>>>>>> 65cd0d2 (Initial Commit)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
<<<<<<< HEAD

# Optional: Function to initialize tables (if needed)
def init_db():
    Base.metadata.create_all(bind=engine)
=======
>>>>>>> 65cd0d2 (Initial Commit)
