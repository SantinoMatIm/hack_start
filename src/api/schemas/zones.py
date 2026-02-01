"""Zone schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ZoneResponse(BaseModel):
    """Response schema for a zone."""

    id: str
    name: str
    slug: str
    latitude: float
    longitude: float
    energy_price_usd_mwh: Optional[float] = None
    fuel_price_usd_mmbtu: Optional[float] = None
    currency: Optional[str] = "USD"
    country_code: Optional[str] = None  # ISO 3166-1 alpha-3 (USA, MEX, SOM)
    state_code: Optional[str] = None  # US state code (TX, CA, AZ)
    created_at: datetime

    class Config:
        from_attributes = True


class ZoneListResponse(BaseModel):
    """Response schema for zone list."""

    zones: list[ZoneResponse]
    total: int


class ZoneEnergyPricesUpdate(BaseModel):
    """Request to update zone energy prices."""

    energy_price_usd_mwh: Optional[float] = Field(
        None, gt=0, description="Electricity price in USD per MWh"
    )
    fuel_price_usd_mmbtu: Optional[float] = Field(
        None, gt=0, description="Fuel price in USD per MMBtu"
    )
    currency: Optional[str] = Field(
        "USD", max_length=10, description="Original currency (for reference)"
    )


class ZoneRegionalCodesUpdate(BaseModel):
    """Request to update zone regional codes for NOAA/EIA data."""

    country_code: Optional[str] = Field(
        None, max_length=3, description="ISO 3166-1 alpha-3 country code (USA, MEX, SOM)"
    )
    state_code: Optional[str] = Field(
        None, max_length=5, description="US state code (TX, CA, AZ) for NOAA & EIA regional data"
    )


class ZoneCreate(BaseModel):
    """Request to create a new zone."""

    name: str = Field(..., min_length=1, max_length=100, description="Zone name")
    slug: str = Field(..., min_length=1, max_length=50, description="URL-friendly identifier")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    country_code: Optional[str] = Field(None, max_length=3, description="Country code (USA, MEX)")
    state_code: Optional[str] = Field(None, max_length=5, description="US state code (TX, CA)")
