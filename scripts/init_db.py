"""Initialize the database with schema and seed data."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.connection import get_engine
from src.db.models import Base


def init_database():
    """Create all tables in the database."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_database()
