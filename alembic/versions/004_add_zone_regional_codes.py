"""Add regional codes to zones for NOAA and EIA data

Revision ID: 004
Revises: 003
Create Date: 2026-02-01 00:00:00.000000

Adds country_code and state_code fields to zones table for US regional data.
- country_code: ISO 3166-1 alpha-3 (USA, MEX, SOM)
- state_code: US state code (TX, CA, AZ) - used for NOAA & EIA regional prices
"""
from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add country code column
    op.add_column(
        "zones",
        sa.Column("country_code", sa.String(3), nullable=True)
    )
    # Add state code column (for US zones)
    op.add_column(
        "zones",
        sa.Column("state_code", sa.String(5), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("zones", "state_code")
    op.drop_column("zones", "country_code")
