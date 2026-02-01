"""Seed power plants and Texas zone for energy infrastructure demo."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.db.connection import get_engine
from src.db.models import Zone, PowerPlant


# Texas zone configuration
TEXAS_ZONE = {
    "name": "Texas Power Region",
    "slug": "texas",
    "latitude": 31.9686,
    "longitude": -99.9018,
    "country_code": "USA",
    "state_code": "TX",
    "energy_price_usd_mwh": 95.0,
    "fuel_price_usd_mmbtu": 3.2,
    "currency": "USD",
}

# Power plants for Texas
TEXAS_POWER_PLANTS = [
    {
        "name": "Comanche Peak Nuclear",
        "plant_type": "nuclear",
        "capacity_mw": 2400,
        "water_dependency": "high",
        "cooling_type": "recirculating",
        "latitude": 32.2987,
        "longitude": -97.7853,
        "operational_status": "active",
    },
    {
        "name": "Martin Lake Steam Station",
        "plant_type": "thermoelectric",
        "capacity_mw": 2250,
        "water_dependency": "high",
        "cooling_type": "once_through",
        "latitude": 32.2606,
        "longitude": -94.5704,
        "operational_status": "active",
    },
    {
        "name": "W.A. Parish Generating Station",
        "plant_type": "thermoelectric",
        "capacity_mw": 3653,
        "water_dependency": "medium",
        "cooling_type": "recirculating",
        "latitude": 29.4843,
        "longitude": -95.6283,
        "operational_status": "active",
    },
    {
        "name": "South Texas Nuclear",
        "plant_type": "nuclear",
        "capacity_mw": 2700,
        "water_dependency": "high",
        "cooling_type": "once_through",
        "latitude": 28.7950,
        "longitude": -96.0489,
        "operational_status": "active",
    },
    {
        "name": "Limestone Electric Generating",
        "plant_type": "thermoelectric",
        "capacity_mw": 1850,
        "water_dependency": "medium",
        "cooling_type": "recirculating",
        "latitude": 31.4167,
        "longitude": -96.2500,
        "operational_status": "active",
    },
]


def seed_texas_zone_and_plants():
    """Insert Texas zone and power plants into the database."""
    engine = get_engine()

    with Session(engine) as session:
        # Check if Texas zone exists
        texas = session.query(Zone).filter(Zone.slug == "texas").first()
        
        if texas:
            print(f"Zone 'texas' already exists (id: {texas.id})")
        else:
            # Create Texas zone
            texas = Zone(
                name=TEXAS_ZONE["name"],
                slug=TEXAS_ZONE["slug"],
                latitude=TEXAS_ZONE["latitude"],
                longitude=TEXAS_ZONE["longitude"],
                country_code=TEXAS_ZONE["country_code"],
                state_code=TEXAS_ZONE["state_code"],
                energy_price_usd_mwh=TEXAS_ZONE["energy_price_usd_mwh"],
                fuel_price_usd_mmbtu=TEXAS_ZONE["fuel_price_usd_mmbtu"],
                currency=TEXAS_ZONE["currency"],
            )
            session.add(texas)
            session.flush()  # Get the ID
            print(f"Created zone: {TEXAS_ZONE['name']} ({TEXAS_ZONE['slug']})")

        # Add power plants
        for plant_data in TEXAS_POWER_PLANTS:
            # Check if plant already exists
            existing = session.query(PowerPlant).filter(
                PowerPlant.zone_id == texas.id,
                PowerPlant.name == plant_data["name"]
            ).first()
            
            if existing:
                print(f"  Plant '{plant_data['name']}' already exists, skipping.")
                continue

            plant = PowerPlant(
                zone_id=texas.id,
                name=plant_data["name"],
                plant_type=plant_data["plant_type"],
                capacity_mw=plant_data["capacity_mw"],
                water_dependency=plant_data["water_dependency"],
                cooling_type=plant_data["cooling_type"],
                latitude=plant_data["latitude"],
                longitude=plant_data["longitude"],
                operational_status=plant_data["operational_status"],
            )
            session.add(plant)
            print(f"  Created plant: {plant_data['name']} ({plant_data['capacity_mw']} MW)")

        session.commit()

    # Summary
    with Session(engine) as session:
        texas = session.query(Zone).filter(Zone.slug == "texas").first()
        plants = session.query(PowerPlant).filter(PowerPlant.zone_id == texas.id).all()
        total_capacity = sum(p.capacity_mw for p in plants)
        
        print("\n" + "=" * 50)
        print(f"Texas Power Region Summary")
        print("=" * 50)
        print(f"Zone ID: {texas.id}")
        print(f"Power Plants: {len(plants)}")
        print(f"Total Capacity: {total_capacity:,.0f} MW")
        print(f"Energy Price: ${texas.energy_price_usd_mwh}/MWh")
        print(f"Fuel Price: ${texas.fuel_price_usd_mmbtu}/MMBtu")
        print("=" * 50)


if __name__ == "__main__":
    seed_texas_zone_and_plants()
