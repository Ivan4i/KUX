"""Initialize SQLite database"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db import engine, Base
from src.database.models import Device, Task, Log
from src.config import get_settings


def init_database():
    """Create all database tables"""
    print("🔧 Initializing database...")

    settings = get_settings()
    print(f"📍 Database URL: {settings.database_url}")

    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    print(f"📁 Data directory: {data_dir}")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("✅ Database initialized successfully!")
    print("\nCreated tables:")
    print("  - devices")
    print("  - tasks")
    print("  - logs")


if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)
