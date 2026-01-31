"""Seed the 15 base actions into the database."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from src.db.connection import get_engine
from src.db.models import Action


# 15 Base Actions Catalog
ACTIONS_CATALOG = [
    # H1: Industrial Reduction (SPI -1.5 to -1.0)
    {
        "code": "H1_INDUSTRIAL_AUDIT",
        "title": "Industrial Water Audit Program",
        "description": "Mandatory water efficiency audits for industrial facilities consuming >10,000 m³/month",
        "heuristic": "H1",
        "spi_min": -1.5,
        "spi_max": -1.0,
        "impact_formula": "5% reduction = +3 days",
        "base_cost": 50000,
        "default_urgency_days": 30,
        "parameter_schema": {
            "reduction_target_pct": {"min": 3, "max": 15, "default": 5},
            "facility_threshold_m3": {"min": 5000, "max": 20000, "default": 10000},
        },
    },
    {
        "code": "H1_RECYCLING_MANDATE",
        "title": "Industrial Water Recycling Mandate",
        "description": "Require industrial water recycling systems for high-consumption sectors",
        "heuristic": "H1",
        "spi_min": -1.5,
        "spi_max": -1.0,
        "impact_formula": "10% recycling = +5 days",
        "base_cost": 200000,
        "default_urgency_days": 45,
        "parameter_schema": {
            "recycling_rate_pct": {"min": 5, "max": 30, "default": 10},
            "sectors_affected": {"options": ["manufacturing", "food_processing", "chemicals"], "default": ["manufacturing"]},
        },
    },
    # H2: Pressure Management (SPI -1.8 to -1.2)
    {
        "code": "H2_PRESSURE_REDUCTION",
        "title": "Network Pressure Reduction",
        "description": "Reduce water distribution pressure during off-peak hours to minimize losses",
        "heuristic": "H2",
        "spi_min": -1.8,
        "spi_max": -1.2,
        "impact_formula": "10% pressure = +4 days",
        "base_cost": 30000,
        "default_urgency_days": 14,
        "parameter_schema": {
            "pressure_reduction_pct": {"min": 5, "max": 20, "default": 10},
            "hours_start": {"min": 22, "max": 23, "default": 23},
            "hours_end": {"min": 5, "max": 7, "default": 6},
        },
    },
    {
        "code": "H2_LEAK_DETECTION",
        "title": "Accelerated Leak Detection Program",
        "description": "Deploy acoustic sensors and prioritize repair of major leaks",
        "heuristic": "H2",
        "spi_min": -1.8,
        "spi_max": -1.2,
        "impact_formula": "1% leak reduction = +2 days",
        "base_cost": 100000,
        "default_urgency_days": 21,
        "parameter_schema": {
            "coverage_pct": {"min": 50, "max": 100, "default": 75},
            "repair_priority_threshold_lps": {"min": 0.5, "max": 2.0, "default": 1.0},
        },
    },
    # H3: Public Communication (SPI -2.0 to -1.0)
    {
        "code": "H3_AWARENESS_CAMPAIGN",
        "title": "Public Awareness Campaign",
        "description": "Multi-channel communication campaign on water conservation",
        "heuristic": "H3",
        "spi_min": -2.0,
        "spi_max": -1.0,
        "impact_formula": "3% reduction = +2 days",
        "base_cost": 25000,
        "default_urgency_days": 7,
        "parameter_schema": {
            "channels": {"options": ["tv", "radio", "social_media", "billboards"], "default": ["social_media", "radio"]},
            "intensity_level": {"options": ["moderate", "high", "emergency"], "default": "moderate"},
        },
    },
    {
        "code": "H3_SCHOOL_PROGRAM",
        "title": "School Water Education Program",
        "description": "Accelerated water conservation education in schools",
        "heuristic": "H3",
        "spi_min": -2.0,
        "spi_max": -1.0,
        "impact_formula": "1% reduction = +0.7 days",
        "base_cost": 15000,
        "default_urgency_days": 14,
        "parameter_schema": {
            "schools_pct": {"min": 30, "max": 100, "default": 50},
            "grade_levels": {"options": ["primary", "secondary", "both"], "default": "both"},
        },
    },
    {
        "code": "H3_HOTLINE_LAUNCH",
        "title": "Water Waste Reporting Hotline",
        "description": "Launch public hotline for reporting water waste and leaks",
        "heuristic": "H3",
        "spi_min": -2.0,
        "spi_max": -1.0,
        "impact_formula": "0.5% reduction = +0.3 days",
        "base_cost": 10000,
        "default_urgency_days": 7,
        "parameter_schema": {
            "response_time_hours": {"min": 2, "max": 24, "default": 12},
            "reward_program": {"options": [True, False], "default": False},
        },
    },
    # H4: Non-Essential Restriction (SPI <= -1.8)
    {
        "code": "H4_LAWN_BAN",
        "title": "Lawn Irrigation Restriction",
        "description": "Restrict lawn and garden irrigation to specific hours/days",
        "heuristic": "H4",
        "spi_min": -999,
        "spi_max": -1.8,
        "impact_formula": "1% removed = +1.3 days",
        "base_cost": 5000,
        "default_urgency_days": 3,
        "parameter_schema": {
            "hours_allowed_per_day": {"min": 0, "max": 4, "default": 2},
            "days_per_week": {"min": 1, "max": 3, "default": 2},
            "compliance_target_pct": {"min": 60, "max": 95, "default": 80},
        },
    },
    {
        "code": "H4_CARWASH_RESTRICTION",
        "title": "Car Wash Water Restriction",
        "description": "Limit commercial car wash operations and ban home car washing",
        "heuristic": "H4",
        "spi_min": -999,
        "spi_max": -1.8,
        "impact_formula": "0.5% removed = +0.65 days",
        "base_cost": 3000,
        "default_urgency_days": 3,
        "parameter_schema": {
            "commercial_days_allowed": {"min": 2, "max": 5, "default": 3},
            "home_wash_ban": {"options": [True, False], "default": True},
        },
    },
    {
        "code": "H4_POOL_RESTRICTION",
        "title": "Swimming Pool Filling Ban",
        "description": "Prohibit filling of private swimming pools",
        "heuristic": "H4",
        "spi_min": -999,
        "spi_max": -1.8,
        "impact_formula": "0.3% removed = +0.4 days",
        "base_cost": 2000,
        "default_urgency_days": 3,
        "parameter_schema": {
            "pool_types_affected": {"options": ["private", "commercial", "all"], "default": "private"},
            "exception_for_public": {"options": [True, False], "default": True},
        },
    },
    {
        "code": "H4_FOUNTAIN_SHUTDOWN",
        "title": "Ornamental Fountain Shutdown",
        "description": "Shut down decorative fountains in public and commercial spaces",
        "heuristic": "H4",
        "spi_min": -999,
        "spi_max": -1.8,
        "impact_formula": "0.2% removed = +0.26 days",
        "base_cost": 1000,
        "default_urgency_days": 1,
        "parameter_schema": {
            "scope": {"options": ["public_only", "commercial_only", "all"], "default": "all"},
        },
    },
    # H5: Source Reallocation (SPI <= -2.0)
    {
        "code": "H5_EMERGENCY_WELLS",
        "title": "Emergency Well Activation",
        "description": "Activate backup groundwater wells for emergency supply",
        "heuristic": "H5",
        "spi_min": -999,
        "spi_max": -2.0,
        "impact_formula": "5% increase = +5 days",
        "base_cost": 150000,
        "default_urgency_days": 7,
        "parameter_schema": {
            "wells_to_activate": {"min": 1, "max": 10, "default": 3},
            "extraction_rate_pct_of_max": {"min": 50, "max": 100, "default": 75},
        },
    },
    {
        "code": "H5_TANKER_DEPLOYMENT",
        "title": "Water Tanker Deployment",
        "description": "Deploy water tankers to critical areas with supply shortages",
        "heuristic": "H5",
        "spi_min": -999,
        "spi_max": -2.0,
        "impact_formula": "2% increase = +2 days",
        "base_cost": 80000,
        "default_urgency_days": 3,
        "parameter_schema": {
            "tankers_count": {"min": 10, "max": 100, "default": 30},
            "priority_areas": {"options": ["hospitals", "schools", "residential", "all"], "default": ["hospitals", "residential"]},
        },
    },
    {
        "code": "H5_INTERBASIN_TRANSFER",
        "title": "Inter-Basin Water Transfer",
        "description": "Negotiate emergency water transfer from neighboring basins",
        "heuristic": "H5",
        "spi_min": -999,
        "spi_max": -2.0,
        "impact_formula": "10% increase = +10 days",
        "base_cost": 500000,
        "default_urgency_days": 14,
        "parameter_schema": {
            "volume_mld": {"min": 50, "max": 500, "default": 100},
            "source_basin": {"options": ["lerma", "cutzamala", "other"], "default": "cutzamala"},
        },
    },
    # H6: Severity Escalation (threshold crossing)
    {
        "code": "H6_EMERGENCY_DECLARATION",
        "title": "Water Emergency Declaration",
        "description": "Formal declaration of water emergency enabling special powers",
        "heuristic": "H6",
        "spi_min": -999,
        "spi_max": 999,
        "impact_formula": "combined effects * 0.8",
        "base_cost": 0,
        "default_urgency_days": 1,
        "parameter_schema": {
            "emergency_level": {"options": ["level_1", "level_2", "level_3"], "default": "level_1"},
            "duration_days": {"min": 7, "max": 90, "default": 30},
        },
    },
]


def seed_actions():
    """Insert base actions into the database."""
    engine = get_engine()

    with Session(engine) as session:
        for action_data in ACTIONS_CATALOG:
            existing = session.query(Action).filter(Action.code == action_data["code"]).first()
            if existing:
                print(f"Action '{action_data['code']}' already exists, skipping.")
                continue

            action = Action(**action_data)
            session.add(action)
            print(f"Created action: {action_data['title']} ({action_data['code']})")

        session.commit()

    print(f"Action seeding completed. Total: {len(ACTIONS_CATALOG)} actions.")


if __name__ == "__main__":
    seed_actions()
