"""Action schemas."""

from typing import Optional, Any
from pydantic import BaseModel


class ActionRequest(BaseModel):
    """Request schema for action details."""

    action_code: str


class ExpectedEffect(BaseModel):
    """Expected effect of an action."""

    days_gained: float
    confidence: str = "estimated"
    formula: Optional[str] = None


class ActionResponse(BaseModel):
    """Response schema for an action."""

    id: str
    code: str
    title: str
    description: Optional[str]
    heuristic: str
    spi_min: float
    spi_max: float
    impact_formula: str
    base_cost: Optional[float]
    default_urgency_days: int
    parameter_schema: Optional[dict]


class RecommendedActionResponse(BaseModel):
    """Response schema for a recommended action."""

    action_instance_id: str  # UUID for simulation
    action_code: str
    title: str
    description: Optional[str]
    heuristic_id: str
    priority_score: float
    parameters: dict
    justification: str
    expected_effect: ExpectedEffect
    method: str = "fallback"  # 'ai' or 'fallback'


class RecommendedActionsRequest(BaseModel):
    """Request schema for recommended actions."""

    zone_id: str
    profile: str  # 'government' or 'industry'


class ContextSummary(BaseModel):
    """Summary of risk context."""

    spi: float
    risk_level: str
    trend: str
    days_to_critical: Optional[int]
    profile: str
    zone: str


class ActivatedHeuristic(BaseModel):
    """Information about an activated heuristic."""

    id: str
    priority: float
    actions_count: int


class RecommendedActionsResponse(BaseModel):
    """Response schema for recommended actions."""

    zone_id: str
    profile: str
    context: ContextSummary
    activated_heuristics: list[ActivatedHeuristic]
    actions: list[RecommendedActionResponse]
