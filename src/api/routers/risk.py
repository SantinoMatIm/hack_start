"""Risk assessment router."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from src.config.settings import get_settings
from src.api.schemas.risk import (
    RiskResponse,
    TrendDetails,
    RiskHistoryResponse,
    RiskSnapshotResponse,
)

router = APIRouter(prefix="/risk", tags=["risk"])


# Demo data for testing without database
DEMO_RISK_DATA = {
    "cdmx": {
        "spi_6m": -1.72,
        "risk_level": "HIGH",
        "trend": "WORSENING",
        "days_to_critical": 24,
    },
    "monterrey": {
        "spi_6m": -1.45,
        "risk_level": "HIGH",
        "trend": "STABLE",
        "days_to_critical": 38,
    },
}


def get_db_session() -> Optional[Session]:
    """Get database session if available, otherwise return None for demo mode."""
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            return None
        from src.db.retry import get_session_with_retry
        return get_session_with_retry()
    except Exception:
        return None


@router.get("/current", response_model=RiskResponse)
def get_current_risk(
    zone_id: str = Query(..., description="Zone ID or slug"),
):
    """
    Get current risk assessment for a zone.

    Returns the latest SPI-6 value, risk level, trend, and days to critical.

    Args:
        zone_id: Zone UUID or slug (e.g., 'cdmx', 'monterrey')
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            # Return demo data
            zone_key = zone_id.lower()
            if zone_key not in DEMO_RISK_DATA:
                raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")
            demo = DEMO_RISK_DATA[zone_key]
            return RiskResponse(
                zone_id=zone_key,
                spi_6m=demo["spi_6m"],
                risk_level=demo["risk_level"],
                trend=demo["trend"],
                days_to_critical=demo["days_to_critical"],
                last_updated=datetime.utcnow().isoformat(),
            )
    except Exception:
        pass

    # Full database mode with retry for transient SSL errors
    from src.db.retry import get_session_with_retry
    from src.db.models import Zone, RiskSnapshot
    from src.ingestion.orchestrator import IngestionOrchestrator
    from src.risk_engine.risk_classifier import RiskClassifier
    from datetime import timedelta

    session = get_session_with_retry()
    try:
        # Get zone
        zone = session.query(Zone).filter(Zone.slug == zone_id).first()
        if not zone:
            try:
                from uuid import UUID
                zone = session.query(Zone).filter(Zone.id == UUID(zone_id)).first()
            except ValueError:
                pass

        if not zone:
            raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

        # Check for recent snapshot (less than 1 day old)
        recent_threshold = datetime.utcnow() - timedelta(days=1)

        recent_snapshot = (
            session.query(RiskSnapshot)
            .filter(RiskSnapshot.zone_id == zone.id)
            .filter(RiskSnapshot.created_at >= recent_threshold)
            .order_by(RiskSnapshot.created_at.desc())
            .first()
        )

        if recent_snapshot:
            # Return cached snapshot
            return RiskResponse(
                zone_id=zone.slug,
                spi_6m=recent_snapshot.spi_6m,
                risk_level=recent_snapshot.risk_level,
                trend=recent_snapshot.trend,
                days_to_critical=recent_snapshot.days_to_critical,
                last_updated=recent_snapshot.created_at.isoformat(),
            )

        # Calculate fresh risk assessment
        try:
            # Get precipitation data
            orchestrator = IngestionOrchestrator(session=session)
            precip_df = orchestrator.get_precipitation_series(zone.id)

            if precip_df.empty:
                raise HTTPException(
                    status_code=400,
                    detail=f"No precipitation data available for zone '{zone_id}'. Run ingestion first.",
                )

            # Calculate risk
            classifier = RiskClassifier(session=session)
            assessment = classifier.assess_risk(
                daily_precip=precip_df,
                zone_id=zone.id,
                save_snapshot=True,
            )

            return RiskResponse(
                zone_id=zone.slug,
                spi_6m=assessment["spi_6m"],
                risk_level=assessment["risk_level"].value,
                trend=assessment["trend"].value,
                days_to_critical=assessment["days_to_critical"],
                trend_details=TrendDetails(**assessment["trend_details"]) if "trend_details" in assessment else None,
                last_updated=assessment["last_updated"],
            )

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.get("/history", response_model=RiskHistoryResponse)
def get_risk_history(
    zone_id: str = Query(..., description="Zone ID or slug"),
    days: int = Query(30, ge=1, le=365, description="Number of days of history"),
):
    """
    Get risk assessment history for a zone.

    Args:
        zone_id: Zone UUID or slug
        days: Number of days of history to retrieve
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            # Return empty history in demo mode
            return RiskHistoryResponse(
                zone_id=zone_id.lower(),
                snapshots=[],
                total=0,
            )
    except Exception:
        pass

    # Full database mode with retry for transient SSL errors
    from src.db.retry import execute_with_retry
    from src.db.models import Zone, RiskSnapshot
    from datetime import timedelta

    def fetch_risk_history(session):
        # Get zone
        zone = session.query(Zone).filter(Zone.slug == zone_id).first()
        if not zone:
            return None, None  # Signal not found
        
        # Get snapshots
        since = datetime.utcnow() - timedelta(days=days)
        
        snapshots = (
            session.query(RiskSnapshot)
            .filter(RiskSnapshot.zone_id == zone.id)
            .filter(RiskSnapshot.created_at >= since)
            .order_by(RiskSnapshot.created_at.desc())
            .all()
        )
        return zone, snapshots

    zone, snapshots = execute_with_retry(fetch_risk_history)
    
    if zone is None:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

    return RiskHistoryResponse(
        zone_id=zone.slug,
        snapshots=[
            RiskSnapshotResponse(
                id=str(s.id),
                spi_6m=s.spi_6m,
                risk_level=s.risk_level,
                trend=s.trend,
                days_to_critical=s.days_to_critical,
                created_at=s.created_at,
            )
            for s in snapshots
        ],
        total=len(snapshots),
    )
