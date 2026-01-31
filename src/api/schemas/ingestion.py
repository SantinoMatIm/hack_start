"""Ingestion schemas."""

from typing import Optional
from pydantic import BaseModel


class IngestionRequest(BaseModel):
    """Request schema for data ingestion."""

    zone_id: Optional[str] = None  # If None, ingest all zones
    sources: list[str] = ["openmeteo"]  # Data sources to use
    force_full: bool = False  # Force full history fetch


class IngestionResultItem(BaseModel):
    """Result for a single ingestion operation."""

    zone: str
    source: str
    records_added: int
    date_range: Optional[str]
    status: str  # 'success', 'up_to_date', 'no_data', 'error'
    error: Optional[str] = None


class IngestionResponse(BaseModel):
    """Response schema for ingestion operation."""

    results: list[IngestionResultItem]
    total_records_added: int
    zones_processed: int
