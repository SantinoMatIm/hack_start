"""Schemas for power plant endpoints."""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class PowerPlantCreate(BaseModel):
    """Request schema for creating a power plant."""

    zone_id: str = Field(..., description="Zone UUID or slug")
    name: str = Field(..., min_length=1, max_length=200)
    plant_type: Literal["thermoelectric", "nuclear", "hydroelectric"] = Field(
        ..., description="Type of power plant"
    )
    capacity_mw: float = Field(..., gt=0, description="Installed capacity in MW")
    water_dependency: Literal["high", "medium", "low"] = Field(
        default="high", description="Level of water dependency"
    )
    cooling_type: str = Field(
        default="recirculating",
        description="Cooling system type: once_through, recirculating, dry",
    )
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class PowerPlantUpdate(BaseModel):
    """Request schema for updating a power plant."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    plant_type: Optional[Literal["thermoelectric", "nuclear", "hydroelectric"]] = None
    capacity_mw: Optional[float] = Field(None, gt=0)
    water_dependency: Optional[Literal["high", "medium", "low"]] = None
    cooling_type: Optional[str] = None
    operational_status: Optional[Literal["active", "maintenance", "offline"]] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class PowerPlantResponse(BaseModel):
    """Response schema for a power plant."""

    id: str
    zone_id: str
    name: str
    plant_type: str
    capacity_mw: float
    water_dependency: str
    cooling_type: str
    latitude: float
    longitude: float
    operational_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PowerPlantListResponse(BaseModel):
    """Response schema for listing power plants."""

    plants: list[PowerPlantResponse]
    total: int
    total_capacity_mw: float
