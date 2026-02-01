"""Add energy price fields to zones

Revision ID: 003
Revises: 002
Create Date: 2026-02-01 00:00:00.000000

Adds optional energy price fields to zones table for local pricing.
"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add energy price columns to zones
    op.add_column(
        "zones",
        sa.Column("energy_price_usd_mwh", sa.Float, nullable=True)
    )
    op.add_column(
        "zones",
        sa.Column("fuel_price_usd_mmbtu", sa.Float, nullable=True)
    )
    op.add_column(
        "zones",
        sa.Column("currency", sa.String(10), nullable=True, server_default="USD")
    )


def downgrade() -> None:
    op.drop_column("zones", "currency")
    op.drop_column("zones", "fuel_price_usd_mmbtu")
    op.drop_column("zones", "energy_price_usd_mwh")
