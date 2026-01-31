"""Ingestion router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.models import Zone
from src.ingestion.orchestrator import IngestionOrchestrator
from src.api.schemas.ingestion import (
    IngestionRequest,
    IngestionResponse,
    IngestionResultItem,
)

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


@router.post("/run", response_model=IngestionResponse)
def run_ingestion(
    request: IngestionRequest,
    session: Session = Depends(get_session),
):
    """
    Trigger data ingestion from climate sources.

    Fetches precipitation data from configured sources (Open-Meteo, NOAA)
    and stores in the database.

    Args:
        request: Ingestion configuration
    """
    orchestrator = IngestionOrchestrator(session=session)

    results = []

    if request.zone_id:
        # Ingest specific zone
        zone = orchestrator.get_zone_by_slug(request.zone_id)
        if not zone:
            raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

        for source in request.sources:
            try:
                if source == "openmeteo":
                    result = orchestrator.ingest_zone_openmeteo(
                        zone=zone,
                        force_full=request.force_full,
                    )
                elif source == "noaa":
                    result = orchestrator.ingest_zone_noaa(
                        zone=zone,
                        force_full=request.force_full,
                    )
                else:
                    result = {
                        "zone": zone.slug,
                        "source": source,
                        "records_added": 0,
                        "status": "error",
                        "error": f"Unknown source: {source}",
                    }

                results.append(IngestionResultItem(
                    zone=result["zone"],
                    source=result["source"],
                    records_added=result.get("records_added", 0),
                    date_range=result.get("date_range"),
                    status=result.get("status", "unknown"),
                    error=result.get("error"),
                ))
            except Exception as e:
                results.append(IngestionResultItem(
                    zone=zone.slug,
                    source=source,
                    records_added=0,
                    date_range=None,
                    status="error",
                    error=str(e),
                ))
    else:
        # Ingest all zones
        ingestion_results = orchestrator.ingest_all_zones(
            sources=request.sources,
            force_full=request.force_full,
        )

        for result in ingestion_results:
            results.append(IngestionResultItem(
                zone=result["zone"],
                source=result["source"],
                records_added=result.get("records_added", 0),
                date_range=result.get("date_range"),
                status=result.get("status", "unknown"),
                error=result.get("error"),
            ))

    # Calculate totals
    total_records = sum(r.records_added for r in results)
    zones_processed = len(set(r.zone for r in results))

    return IngestionResponse(
        results=results,
        total_records_added=total_records,
        zones_processed=zones_processed,
    )
