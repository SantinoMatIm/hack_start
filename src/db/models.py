"""SQLAlchemy ORM models for the Water Risk Platform."""

import uuid
from datetime import datetime, date
from typing import Optional

from sqlalchemy import (
    String,
    Float,
    Integer,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Text,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class Zone(Base):
    """Geographic zones for monitoring (pilot: CDMX, Monterrey)."""

    __tablename__ = "zones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    climate_data: Mapped[list["ClimateTimeseries"]] = relationship(
        back_populates="zone", cascade="all, delete-orphan"
    )
    risk_snapshots: Mapped[list["RiskSnapshot"]] = relationship(
        back_populates="zone", cascade="all, delete-orphan"
    )
    action_instances: Mapped[list["ActionInstance"]] = relationship(
        back_populates="zone", cascade="all, delete-orphan"
    )
    simulations: Mapped[list["Simulation"]] = relationship(
        back_populates="zone", cascade="all, delete-orphan"
    )


class ClimateTimeseries(Base):
    """Time series climate data from various sources."""

    __tablename__ = "climate_timeseries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False
    )
    variable: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., 'precipitation', 'temperature'
    date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'openmeteo', 'noaa'
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    zone: Mapped["Zone"] = relationship(back_populates="climate_data")

    __table_args__ = (
        UniqueConstraint("zone_id", "variable", "date", "source", name="uq_climate_data"),
    )


class RiskSnapshot(Base):
    """Point-in-time risk assessment snapshots."""

    __tablename__ = "risk_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False
    )
    spi_6m: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # LOW, MEDIUM, HIGH, CRITICAL
    trend: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # IMPROVING, STABLE, WORSENING
    days_to_critical: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    zone: Mapped["Zone"] = relationship(back_populates="risk_snapshots")
    simulations: Mapped[list["Simulation"]] = relationship(
        back_populates="input_snapshot"
    )


class Action(Base):
    """Base action catalog (15 predefined actions)."""

    __tablename__ = "actions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    heuristic: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # H1, H2, etc.
    spi_min: Mapped[float] = mapped_column(Float, nullable=False)
    spi_max: Mapped[float] = mapped_column(Float, nullable=False)
    impact_formula: Mapped[str] = mapped_column(
        String(200), nullable=False
    )  # e.g., "5% reduction = +3 days"
    base_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    default_urgency_days: Mapped[int] = mapped_column(Integer, nullable=False)
    parameter_schema: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    instances: Mapped[list["ActionInstance"]] = relationship(
        back_populates="base_action", cascade="all, delete-orphan"
    )


class ActionInstance(Base):
    """Parameterized action instances for specific zones and contexts."""

    __tablename__ = "action_instances"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False
    )
    base_action_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("actions.id"), nullable=False
    )
    profile: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # government, industry
    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    justification: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expected_effect: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True
    )  # e.g., {"days_gained": 5}
    priority_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    zone: Mapped["Zone"] = relationship(back_populates="action_instances")
    base_action: Mapped["Action"] = relationship(back_populates="instances")


class Simulation(Base):
    """Scenario simulations comparing act vs. no-act outcomes."""

    __tablename__ = "simulations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    zone_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False
    )
    scenario_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'no_action', 'with_action'
    input_snapshot_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("risk_snapshots.id"), nullable=False
    )
    action_instance_ids: Mapped[Optional[list]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=True
    )
    future_spi: Mapped[float] = mapped_column(Float, nullable=False)
    future_risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    days_to_critical: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    projection_days: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relationships
    zone: Mapped["Zone"] = relationship(back_populates="simulations")
    input_snapshot: Mapped["RiskSnapshot"] = relationship(back_populates="simulations")
