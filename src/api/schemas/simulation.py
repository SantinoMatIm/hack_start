"""Simulation schemas."""

from typing import Optional
from pydantic import BaseModel


class TrajectoryPoint(BaseModel):
    """Point in a trajectory projection."""

    day: int
    projected_spi: float
    risk_level: str
    improvement_applied: Optional[float] = None


class ScenarioResult(BaseModel):
    """Result of a single scenario."""

    ending_spi: float
    ending_risk_level: str
    days_to_critical: Optional[int]
    trajectory: list[TrajectoryPoint]


class ScenarioComparison(BaseModel):
    """Comparison metrics between scenarios."""

    days_gained: int
    spi_improvement: float
    risk_level_change: str
    actions_count: int


class SimulationRequest(BaseModel):
    """Request schema for simulation."""

    zone_id: str
    action_instance_ids: list[str]  # UUIDs of ActionInstances (from recommended actions)
    projection_days: int = 90


class ActionApplied(BaseModel):
    """Action with its simulated impact."""

    code: str
    title: str
    days_gained: float


class SimulationResponse(BaseModel):
    """Response schema for simulation results."""

    zone_id: str
    no_action: ScenarioResult
    with_action: ScenarioResult
    comparison: ScenarioComparison
    summary: str  # Human-readable summary
    actions_applied: list[ActionApplied] = []  # Per-action impact for dashboard
