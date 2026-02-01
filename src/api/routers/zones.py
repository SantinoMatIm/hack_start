"""Zones router."""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.api.schemas.zones import ZoneResponse, ZoneListResponse, ZoneEnergyPricesUpdate, ZoneRegionalCodesUpdate, ZoneCreate

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


@router.post("", response_model=ZoneResponse)
def create_zone(request: ZoneCreate):
    """
    Create a new zone.

    For US zones, set country_code="USA" and state_code (e.g., "TX").
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Creating zones requires database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import Zone

    session = next(get_session())

    # Check if slug already exists
    existing = session.query(Zone).filter(Zone.slug == request.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Zone with slug '{request.slug}' already exists")

    zone = Zone(
        name=request.name,
        slug=request.slug,
        latitude=request.latitude,
        longitude=request.longitude,
        country_code=request.country_code.upper() if request.country_code else None,
        state_code=request.state_code.upper() if request.state_code else None,
    )
    session.add(zone)
    session.commit()
    session.refresh(zone)

    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        slug=zone.slug,
        latitude=zone.latitude,
        longitude=zone.longitude,
        energy_price_usd_mwh=zone.energy_price_usd_mwh,
        fuel_price_usd_mmbtu=zone.fuel_price_usd_mmbtu,
        currency=zone.currency,
        country_code=zone.country_code,
        state_code=zone.state_code,
        created_at=zone.created_at,
    )


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

    # Full database mode with retry for transient errors
    from src.db.retry import execute_with_retry
    from src.db.models import Zone

    def fetch_zones(session):
        return session.query(Zone).all()

    zones = execute_with_retry(fetch_zones)

    return ZoneListResponse(
        zones=[
            ZoneResponse(
                id=str(zone.id),
                name=zone.name,
                slug=zone.slug,
                latitude=zone.latitude,
                longitude=zone.longitude,
                energy_price_usd_mwh=zone.energy_price_usd_mwh,
                fuel_price_usd_mmbtu=zone.fuel_price_usd_mmbtu,
                currency=zone.currency,
                country_code=zone.country_code,
                state_code=zone.state_code,
                created_at=zone.created_at,
            )
            for zone in zones
        ],
        total=len(zones),
    )


@router.get("/debug/counts")
def get_table_counts():
    """Debug endpoint to check table counts."""
    from src.db.retry import execute_with_retry
    from src.db.models import Zone, PrecipitationRecord, RiskSnapshot, Action, ActionInstance

    def fetch_counts(session):
        return {
            "zones": session.query(Zone).count(),
            "precipitation_records": session.query(PrecipitationRecord).count(),
            "risk_snapshots": session.query(RiskSnapshot).count(),
            "actions": session.query(Action).count(),
            "action_instances": session.query(ActionInstance).count(),
        }

    return execute_with_retry(fetch_counts)


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

    # Full database mode with retry for transient errors
    from src.db.retry import execute_with_retry
    from src.db.models import Zone
    from uuid import UUID as PyUUID

    def fetch_zone(session):
        # Try by slug first
        zone = session.query(Zone).filter(Zone.slug == zone_id).first()
        # Try by UUID if not found
        if not zone:
            try:
                zone = session.query(Zone).filter(Zone.id == PyUUID(zone_id)).first()
            except ValueError:
                pass
        return zone

    zone = execute_with_retry(fetch_zone)

    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        slug=zone.slug,
        latitude=zone.latitude,
        longitude=zone.longitude,
        energy_price_usd_mwh=zone.energy_price_usd_mwh,
        fuel_price_usd_mmbtu=zone.fuel_price_usd_mmbtu,
        currency=zone.currency,
        country_code=zone.country_code,
        state_code=zone.state_code,
        created_at=zone.created_at,
    )


@router.patch("/{zone_id}/energy-prices", response_model=ZoneResponse)
def update_zone_energy_prices(zone_id: str, request: ZoneEnergyPricesUpdate):
    """
    Update energy prices for a zone.

    Set local electricity and fuel prices for economic simulations.
    If not set, EIA API prices (US average) will be used as fallback.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Energy prices require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import Zone
    from uuid import UUID

    session = next(get_session())

    # Find zone
    zone = session.query(Zone).filter(Zone.slug == zone_id).first()
    if not zone:
        try:
            zone = session.query(Zone).filter(Zone.id == UUID(zone_id)).first()
        except ValueError:
            pass

    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

    # Update prices
    if request.energy_price_usd_mwh is not None:
        zone.energy_price_usd_mwh = request.energy_price_usd_mwh
    if request.fuel_price_usd_mmbtu is not None:
        zone.fuel_price_usd_mmbtu = request.fuel_price_usd_mmbtu
    if request.currency is not None:
        zone.currency = request.currency

    session.commit()
    session.refresh(zone)

    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        slug=zone.slug,
        latitude=zone.latitude,
        longitude=zone.longitude,
        energy_price_usd_mwh=zone.energy_price_usd_mwh,
        fuel_price_usd_mmbtu=zone.fuel_price_usd_mmbtu,
        currency=zone.currency,
        country_code=zone.country_code,
        state_code=zone.state_code,
        created_at=zone.created_at,
    )


@router.patch("/{zone_id}/regional-codes", response_model=ZoneResponse)
def update_zone_regional_codes(zone_id: str, request: ZoneRegionalCodesUpdate):
    """
    Update regional codes for a zone.

    Set country_code and state_code for US zones to enable:
    - NOAA precipitation data from correct US state
    - EIA regional electricity and fuel prices
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Regional codes require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import Zone
    from uuid import UUID

    session = next(get_session())

    # Find zone
    zone = session.query(Zone).filter(Zone.slug == zone_id).first()
    if not zone:
        try:
            zone = session.query(Zone).filter(Zone.id == UUID(zone_id)).first()
        except ValueError:
            pass

    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")

    # Update regional codes
    if request.country_code is not None:
        zone.country_code = request.country_code.upper()
    if request.state_code is not None:
        zone.state_code = request.state_code.upper()

    session.commit()
    session.refresh(zone)

    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        slug=zone.slug,
        latitude=zone.latitude,
        longitude=zone.longitude,
        energy_price_usd_mwh=zone.energy_price_usd_mwh,
        fuel_price_usd_mmbtu=zone.fuel_price_usd_mmbtu,
        currency=zone.currency,
        country_code=zone.country_code,
        state_code=zone.state_code,
        created_at=zone.created_at,
    )