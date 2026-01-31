"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create zones table
    op.create_table(
        "zones",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(50), unique=True, nullable=False),
        sa.Column("latitude", sa.Float, nullable=False),
        sa.Column("longitude", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create climate_timeseries table
    op.create_table(
        "climate_timeseries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("zone_id", UUID(as_uuid=True), sa.ForeignKey("zones.id"), nullable=False),
        sa.Column("variable", sa.String(50), nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("zone_id", "variable", "date", "source", name="uq_climate_data"),
    )

    # Create risk_snapshots table
    op.create_table(
        "risk_snapshots",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("zone_id", UUID(as_uuid=True), sa.ForeignKey("zones.id"), nullable=False),
        sa.Column("spi_6m", sa.Float, nullable=False),
        sa.Column("risk_level", sa.String(20), nullable=False),
        sa.Column("trend", sa.String(20), nullable=False),
        sa.Column("days_to_critical", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create actions table
    op.create_table(
        "actions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("code", sa.String(50), unique=True, nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("heuristic", sa.String(50), nullable=False),
        sa.Column("spi_min", sa.Float, nullable=False),
        sa.Column("spi_max", sa.Float, nullable=False),
        sa.Column("impact_formula", sa.String(200), nullable=False),
        sa.Column("base_cost", sa.Float, nullable=True),
        sa.Column("default_urgency_days", sa.Integer, nullable=False),
        sa.Column("parameter_schema", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create action_instances table
    op.create_table(
        "action_instances",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("zone_id", UUID(as_uuid=True), sa.ForeignKey("zones.id"), nullable=False),
        sa.Column("base_action_id", UUID(as_uuid=True), sa.ForeignKey("actions.id"), nullable=False),
        sa.Column("profile", sa.String(20), nullable=False),
        sa.Column("parameters", JSONB, nullable=True),
        sa.Column("justification", sa.Text, nullable=True),
        sa.Column("expected_effect", JSONB, nullable=True),
        sa.Column("priority_score", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create simulations table
    op.create_table(
        "simulations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("zone_id", UUID(as_uuid=True), sa.ForeignKey("zones.id"), nullable=False),
        sa.Column("scenario_type", sa.String(20), nullable=False),
        sa.Column("input_snapshot_id", UUID(as_uuid=True), sa.ForeignKey("risk_snapshots.id"), nullable=False),
        sa.Column("action_instance_ids", ARRAY(UUID(as_uuid=True)), nullable=True),
        sa.Column("future_spi", sa.Float, nullable=False),
        sa.Column("future_risk_level", sa.String(20), nullable=False),
        sa.Column("days_to_critical", sa.Integer, nullable=True),
        sa.Column("projection_days", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("now()"), nullable=False),
    )

    # Create indexes
    op.create_index("ix_climate_timeseries_zone_date", "climate_timeseries", ["zone_id", "date"])
    op.create_index("ix_risk_snapshots_zone_created", "risk_snapshots", ["zone_id", "created_at"])
    op.create_index("ix_actions_heuristic", "actions", ["heuristic"])


def downgrade() -> None:
    op.drop_table("simulations")
    op.drop_table("action_instances")
    op.drop_table("actions")
    op.drop_table("risk_snapshots")
    op.drop_table("climate_timeseries")
    op.drop_table("zones")
