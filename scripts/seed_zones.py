"""Seed pilot zones (CDMX and Monterrey)."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.db.connection import get_engine
from src.db.models import Zone
from src.config.constants import PILOT_ZONES


def seed_zones():
    """Insert pilot zones into the database."""
    engine = get_engine()

    with Session(engine) as session:
        for slug, data in PILOT_ZONES.items():
            existing = session.query(Zone).filter(Zone.slug == slug).first()
            if existing:
                print(f"Zone '{slug}' already exists, skipping.")
                continue

            zone = Zone(
                name=data["name"],
                slug=slug,
                latitude=data["latitude"],
                longitude=data["longitude"],
            )
            session.add(zone)
            print(f"Created zone: {data['name']} ({slug})")

        session.commit()

    print("Zone seeding completed.")


if __name__ == "__main__":
    seed_zones()
