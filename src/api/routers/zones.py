"""Zones router."""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.api.schemas.zones import ZoneResponse, ZoneListResponse

router = APIRouter(prefix="/zones", tags=["zones"])


# Demo zones data
DEMO_ZONES = [
    {
        "id": "demo-cdmx",
        "name": "Mexico City Metropolitan Area",
        "slug": "cdmx",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "created_at": datetime(2024, 1, 1),
    },
    {
        "id": "demo-monterrey",
        "name": "Monterrey Metropolitan Area",
        "slug": "monterrey",
        "latitude": 25.6866,
        "longitude": -100.3161,
        "created_at": datetime(2024, 1, 1),
    },
]


@router.get("", response_model=ZoneListResponse)
def list_zones():
    """
    List all available zones.

    Returns all configured monitoring zones (CDMX, Monterrey).
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            return ZoneListResponse(
                zones=[ZoneResponse(**z) for z in DEMO_ZONES],
                total=len(DEMO_ZONES),
            )
    except Exception:
        pass

    # Full database mode
    from src.db.connection import get_session
    from src.db.models import Zone

    session = next(get_session())
    zones = session.query(Zone).all()

    return ZoneListResponse(
        zones=[
            ZoneResponse(
                id=str(zone.id),
                name=zone.name,
                slug=zone.slug,
                latitude=zone.latitude,
                longitude=zone.longitude,
                created_at=zone.created_at,
            )
            for zone in zones
        ],
        total=len(zones),
    )


@router.get("/debug/counts")
def get_table_counts():
    """Debug endpoint to check table counts."""
    from src.db.connection import get_session
    from src.db.models import Zone, PrecipitationRecord, RiskSnapshot, Action, ActionInstance

    session = next(get_session())

    return {
        "zones": session.query(Zone).count(),
        "precipitation_records": session.query(PrecipitationRecord).count(),
        "risk_snapshots": session.query(RiskSnapshot).count(),
        "actions": session.query(Action).count(),
        "action_instances": session.query(ActionInstance).count(),
    }


@router.get("/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: str):
    """
    Get a specific zone by ID or slug.

    Args:
        zone_id: Zone UUID or slug
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            for z in DEMO_ZONES:
                if z["slug"] == zone_id.lower() or z["id"] == zone_id:
                    return ZoneResponse(**z)
            raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")
    except HTTPException:
        raise
    except Exception:
        pass

    # Full database mode
    from src.db.connection import get_session
    from src.db.models import Zone

    session = next(get_session())

    # Try by slug first
    zone = session.query(Zone).filter(Zone.slug == zone_id).first()

    # Try by UUID if not found
    if not zone:
        try:
            from uuid import UUID
            zone = session.query(Zone).filter(Zone.id == UUID(zone_id)).first()
        except ValueError:
            pass

    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        slug=zone.slug,
        latitude=zone.latitude,
        longitude=zone.longitude,
        created_at=zone.created_at,
    )
