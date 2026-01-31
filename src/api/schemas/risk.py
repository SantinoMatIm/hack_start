"""Risk assessment schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TrendDetails(BaseModel):
    """Detailed trend information."""

    spi_change_2w: float
    monthly_rate: float
    rapid_deterioration: bool
    recent_3m_min: float
    recent_3m_max: float
    recent_3m_avg: float


class RiskResponse(BaseModel):
    """Response schema for current risk assessment."""

    zone_id: str
    spi_6m: float
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    trend: str  # IMPROVING, STABLE, WORSENING
    days_to_critical: Optional[int]
    trend_details: Optional[TrendDetails] = None
    last_updated: str


class RiskSnapshotResponse(BaseModel):
    """Response schema for a risk snapshot."""

    id: str
    spi_6m: float
    risk_level: str
    trend: str
    days_to_critical: Optional[int]
    created_at: datetime


class RiskHistoryResponse(BaseModel):
    """Response schema for risk history."""

    zone_id: str
    snapshots: list[RiskSnapshotResponse]
    total: int
