"""Zone schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ZoneResponse(BaseModel):
    """Response schema for a zone."""

    id: str
    name: str
    slug: str
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        from_attributes = True


class ZoneListResponse(BaseModel):
    """Response schema for zone list."""

    zones: list[ZoneResponse]
    total: int
