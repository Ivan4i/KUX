"""Database setup and connection"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Database URL (SQLite for MVP)
DATABASE_URL = "sqlite:///./data/sqlite.db"

# Create data directory if it doesn't exist
data_dir = Path(__file__).parent.parent.parent / "data"
data_dir.mkdir(exist_ok=True)

# Create engine with SQLite-specific options
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for ORM models
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
