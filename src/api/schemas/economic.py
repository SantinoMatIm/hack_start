"""Schemas for economic simulation endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EnergyPricesResponse(BaseModel):
    """Current energy prices from EIA."""

    marginal_price_usd_mwh: float = Field(
        ..., description="Average retail electricity price (USD per MWh)"
    )
    fuel_price_usd_mmbtu: float = Field(
        ..., description="Natural gas spot price (USD per MMBtu)"
    )
    fetched_at: str = Field(..., description="When prices were fetched")
    source: str = Field(default="eia", description="Data source")


class EconomicSimulationRequest(BaseModel):
    """Request schema for economic simulation."""

    zone_id: str = Field(..., description="Zone UUID or slug")
    power_plant_ids: list[str] = Field(
        default=[],
        description="UUIDs of power plants to simulate. Empty = all plants in zone.",
    )
    action_instance_ids: list[str] = Field(
        default=[],
        description="Action instance UUIDs to apply. Empty = use recommended.",
    )
    projection_days: int = Field(
        default=90, ge=1, le=365, description="Days to project forward"
    )


class EconomicScenarioResult(BaseModel):
    """Result for a single economic scenario."""

    capacity_loss_pct: float = Field(
        ..., description="Average capacity loss as decimal (0.0 - 1.0)"
    )
    total_cost_usd: float = Field(..., description="Total cost in USD")
    emergency_fuel_cost_usd: float = Field(
        ..., description="Emergency fuel purchase cost"
    )
    lost_generation_mwh: float = Field(..., description="Total MWh not generated")


class PlantBreakdown(BaseModel):
    """Per-plant economic breakdown."""

    plant_id: str
    plant_name: str
    capacity_mw: float
    no_action_cost_usd: float
    with_action_cost_usd: float
    savings_usd: float
    capacity_loss_no_action: float
    capacity_loss_with_action: float


class EconomicSimulationResponse(BaseModel):
    """Response schema for economic simulation."""

    zone_id: str
    plants_analyzed: int
    total_capacity_mw: float

    # Scenario comparison
    no_action: EconomicScenarioResult
    with_action: EconomicScenarioResult

    # Savings
    savings_usd: float = Field(..., description="Total savings in USD")
    savings_pct: float = Field(..., description="Savings as percentage of no-action cost")

    # Summary
    summary: str = Field(..., description="Human-readable summary")

    # Per-plant details
    per_plant_breakdown: list[PlantBreakdown] = Field(default=[])

    # Prices used
    marginal_price_used_usd_mwh: float
    fuel_price_used_usd_mmbtu: float
    projection_days: int
    calculated_at: str


class EnergyPriceHistoryPoint(BaseModel):
    """A single point in price history."""

    period: str
    price_usd_mwh: Optional[float] = None
    price_usd_mmbtu: Optional[float] = None


class EnergyPriceHistoryResponse(BaseModel):
    """Historical energy prices."""

    region: str
    price_type: str
    history: list[EnergyPriceHistoryPoint]
    total: int
