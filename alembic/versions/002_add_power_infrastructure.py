"""Add power infrastructure tables

Revision ID: 002
Revises: 001
Create Date: 2026-02-01 00:00:00.000000

Adds tables for:
- power_plants: Power plants dependent on water for cooling
- energy_price_cache: Cached energy prices from EIA API
- economic_simulations: Economic impact simulation results
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create power_plants table
    op.create_table(
        "power_plants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("zone_id", UUID(as_uuid=True), sa.ForeignKey("zones.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("plant_type", sa.String(50), nullable=False),  # thermoelectric, nuclear, hydroelectric
        sa.Column("capacity_mw", sa.Float, nullable=False),
        sa.Column("water_dependency", sa.String(20), nullable=False, server_default="high"),  # high, medium, low
        sa.Column("cooling_type", sa.String(50), nullable=False, server_default="recirculating"),  # once_through, recirculating, dry
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("operational_status", sa.String(20), nullable=False, server_default="active"),  # active, maintenance, offline
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create energy_price_cache table
    op.create_table(
        "energy_price_cache",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("region", sa.String(50), nullable=False),
        sa.Column("price_type", sa.String(50), nullable=False),  # retail, wholesale, fuel
        sa.Column("value_usd", sa.Float, nullable=False),
        sa.Column("unit", sa.String(20), nullable=False),  # MWh, MMBtu
        sa.Column("source", sa.String(20), nullable=False, server_default="eia"),
        sa.Column("fetched_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.Column("valid_until", sa.DateTime, nullable=False),
        sa.UniqueConstraint("region", "price_type", "source", name="uq_energy_price"),
    )

    # Create economic_simulations table
    op.create_table(
        "economic_simulations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("simulation_id", UUID(as_uuid=True), sa.ForeignKey("simulations.id"), nullable=True),
        sa.Column("power_plant_id", UUID(as_uuid=True), sa.ForeignKey("power_plants.id"), nullable=False),
        sa.Column("capacity_loss_pct", sa.Float, nullable=False),
        sa.Column("cost_no_action_usd", sa.Float, nullable=False),
        sa.Column("cost_with_action_usd", sa.Float, nullable=False),
        sa.Column("savings_usd", sa.Float, nullable=False),
        sa.Column("emergency_fuel_cost_usd", sa.Float, nullable=False),
        sa.Column("marginal_price_used", sa.Float, nullable=False),
        sa.Column("fuel_price_used", sa.Float, nullable=False),
        sa.Column("projection_days", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create indexes
    op.create_index("ix_power_plants_zone", "power_plants", ["zone_id"])
    op.create_index("ix_power_plants_type", "power_plants", ["plant_type"])
    op.create_index("ix_energy_price_cache_region", "energy_price_cache", ["region", "price_type"])
    op.create_index("ix_economic_simulations_plant", "economic_simulations", ["power_plant_id"])


def downgrade() -> None:
    op.drop_table("economic_simulations")
    op.drop_table("energy_price_cache")
    op.drop_table("power_plants")
