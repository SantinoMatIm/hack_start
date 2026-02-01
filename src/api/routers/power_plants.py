"""Power plants router for managing power infrastructure."""

from fastapi import APIRouter, HTTPException, Query
from uuid import UUID

from src.config.settings import get_settings
from src.api.schemas.power_plants import (
    PowerPlantCreate,
    PowerPlantUpdate,
    PowerPlantResponse,
    PowerPlantListResponse,
)

router = APIRouter(prefix="/plants", tags=["power-plants"])


@router.get("", response_model=PowerPlantListResponse)
def list_power_plants(
    zone_id: str = Query(None, description="Filter by zone UUID or slug"),
):
    """
    List all power plants, optionally filtered by zone.

    Returns plants with their capacity and operational status.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Power plants require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import PowerPlant, Zone

    session = next(get_session())

    query = session.query(PowerPlant)

    if zone_id:
        # Try by slug first
        zone = session.query(Zone).filter(Zone.slug == zone_id).first()
        if not zone:
            try:
                zone = session.query(Zone).filter(Zone.id == UUID(zone_id)).first()
            except ValueError:
                pass
        if not zone:
            raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found")
        query = query.filter(PowerPlant.zone_id == zone.id)

    plants = query.all()
    total_capacity = sum(p.capacity_mw for p in plants)

    return PowerPlantListResponse(
        plants=[
            PowerPlantResponse(
                id=str(p.id),
                zone_id=str(p.zone_id),
                name=p.name,
                plant_type=p.plant_type,
                capacity_mw=p.capacity_mw,
                water_dependency=p.water_dependency,
                cooling_type=p.cooling_type,
                latitude=p.latitude,
                longitude=p.longitude,
                operational_status=p.operational_status,
                created_at=p.created_at,
            )
            for p in plants
        ],
        total=len(plants),
        total_capacity_mw=total_capacity,
    )


@router.post("", response_model=PowerPlantResponse, status_code=201)
def create_power_plant(request: PowerPlantCreate):
    """
    Create a new power plant.

    Links the plant to a zone for water risk monitoring.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Power plants require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import PowerPlant, Zone

    session = next(get_session())

    # Find zone
    zone = session.query(Zone).filter(Zone.slug == request.zone_id).first()
    if not zone:
        try:
            zone = session.query(Zone).filter(Zone.id == UUID(request.zone_id)).first()
        except ValueError:
            pass
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

    # Create plant
    plant = PowerPlant(
        zone_id=zone.id,
        name=request.name,
        plant_type=request.plant_type,
        capacity_mw=request.capacity_mw,
        water_dependency=request.water_dependency,
        cooling_type=request.cooling_type,
        latitude=request.latitude,
        longitude=request.longitude,
        operational_status="active",
    )

    session.add(plant)
    session.commit()
    session.refresh(plant)

    return PowerPlantResponse(
        id=str(plant.id),
        zone_id=str(plant.zone_id),
        name=plant.name,
        plant_type=plant.plant_type,
        capacity_mw=plant.capacity_mw,
        water_dependency=plant.water_dependency,
        cooling_type=plant.cooling_type,
        latitude=plant.latitude,
        longitude=plant.longitude,
        operational_status=plant.operational_status,
        created_at=plant.created_at,
    )


@router.get("/{plant_id}", response_model=PowerPlantResponse)
def get_power_plant(plant_id: str):
    """
    Get details of a specific power plant.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Power plants require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import PowerPlant

    session = next(get_session())

    try:
        plant = session.query(PowerPlant).filter(PowerPlant.id == UUID(plant_id)).first()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid plant ID format")

    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_id}' not found")

    return PowerPlantResponse(
        id=str(plant.id),
        zone_id=str(plant.zone_id),
        name=plant.name,
        plant_type=plant.plant_type,
        capacity_mw=plant.capacity_mw,
        water_dependency=plant.water_dependency,
        cooling_type=plant.cooling_type,
        latitude=plant.latitude,
        longitude=plant.longitude,
        operational_status=plant.operational_status,
        created_at=plant.created_at,
    )


@router.patch("/{plant_id}", response_model=PowerPlantResponse)
def update_power_plant(plant_id: str, request: PowerPlantUpdate):
    """
    Update a power plant's details.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Power plants require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import PowerPlant

    session = next(get_session())

    try:
        plant = session.query(PowerPlant).filter(PowerPlant.id == UUID(plant_id)).first()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid plant ID format")

    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_id}' not found")

    # Update fields if provided
    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plant, field, value)

    session.commit()
    session.refresh(plant)

    return PowerPlantResponse(
        id=str(plant.id),
        zone_id=str(plant.zone_id),
        name=plant.name,
        plant_type=plant.plant_type,
        capacity_mw=plant.capacity_mw,
        water_dependency=plant.water_dependency,
        cooling_type=plant.cooling_type,
        latitude=plant.latitude,
        longitude=plant.longitude,
        operational_status=plant.operational_status,
        created_at=plant.created_at,
    )


@router.delete("/{plant_id}", status_code=204)
def delete_power_plant(plant_id: str):
    """
    Delete a power plant.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Power plants require database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import PowerPlant

    session = next(get_session())

    try:
        plant = session.query(PowerPlant).filter(PowerPlant.id == UUID(plant_id)).first()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid plant ID format")

    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant '{plant_id}' not found")

    session.delete(plant)
    session.commit()

    return None
