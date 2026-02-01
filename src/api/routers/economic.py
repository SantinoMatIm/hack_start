"""Economic simulation router for power infrastructure analysis."""

from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.config.settings import get_settings
from src.api.schemas.economic import (
    EnergyPricesResponse,
    EconomicSimulationRequest,
    EconomicSimulationResponse,
    EconomicScenarioResult,
    PlantBreakdown,
    EnergyPriceHistoryResponse,
    EnergyPriceHistoryPoint,
)

router = APIRouter(prefix="/economic", tags=["economic"])


@router.get("/prices", response_model=EnergyPricesResponse)
def get_current_prices(
    region: str = Query("US", description="Region code (e.g., US, TX, CA)"),
):
    """
    Get current energy prices from EIA API.

    Returns:
    - marginal_price_usd_mwh: Retail electricity price
    - fuel_price_usd_mmbtu: Natural gas spot price
    """
    settings = get_settings()

    if not settings.eia_api_key:
        # Return fallback prices if no API key
        return EnergyPricesResponse(
            marginal_price_usd_mwh=100.0,  # ~10 cents/kWh
            fuel_price_usd_mmbtu=3.0,  # Typical natural gas price
            fetched_at=datetime.utcnow().isoformat(),
            source="fallback",
        )

    try:
        from src.ingestion.eia_source import EIAClient

        client = EIAClient(api_key=settings.eia_api_key)
        prices = client.get_current_prices()

        return EnergyPricesResponse(
            marginal_price_usd_mwh=prices["marginal_price_usd_mwh"],
            fuel_price_usd_mmbtu=prices["fuel_price_usd_mmbtu"],
            fetched_at=prices["fetched_at"],
            source="eia",
        )
    except Exception as e:
        # Fallback on error
        return EnergyPricesResponse(
            marginal_price_usd_mwh=100.0,
            fuel_price_usd_mmbtu=3.0,
            fetched_at=datetime.utcnow().isoformat(),
            source=f"fallback (EIA error: {str(e)[:50]})",
        )


@router.post("/simulate", response_model=EconomicSimulationResponse)
def simulate_economic_impact(request: EconomicSimulationRequest):
    """
    Simulate economic impact of water stress on power plants.

    Compares two scenarios:
    - No Action: Water stress continues, plants lose capacity
    - With Action: Water interventions reduce stress, less capacity loss

    Returns savings in USD and percentage.
    """
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Economic simulation requires database. Configure DATABASE_URL.",
        )

    from src.db.connection import get_session
    from src.db.models import Zone, PowerPlant, RiskSnapshot, EconomicSimulation
    from src.economic.cost_calculator import EconomicCostCalculator
    from src.simulation.scenario_builder import ScenarioBuilder
    from src.config.constants import Trend

    session = next(get_session())

    # Get zone
    zone = session.query(Zone).filter(Zone.slug == request.zone_id).first()
    if not zone:
        try:
            zone = session.query(Zone).filter(Zone.id == UUID(request.zone_id)).first()
        except ValueError:
            pass
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

    # Get latest risk snapshot for the zone
    snapshot = (
        session.query(RiskSnapshot)
        .filter(RiskSnapshot.zone_id == zone.id)
        .order_by(RiskSnapshot.created_at.desc())
        .first()
    )
    if not snapshot:
        raise HTTPException(
            status_code=400,
            detail=f"No risk assessment for zone '{request.zone_id}'. Run risk assessment first.",
        )

    # Get power plants
    if request.power_plant_ids:
        plants = []
        for pid in request.power_plant_ids:
            try:
                plant = session.query(PowerPlant).filter(
                    PowerPlant.id == UUID(pid),
                    PowerPlant.zone_id == zone.id,
                ).first()
                if plant:
                    plants.append(plant)
            except ValueError:
                continue
    else:
        # All plants in zone
        plants = session.query(PowerPlant).filter(PowerPlant.zone_id == zone.id).all()

    if not plants:
        raise HTTPException(
            status_code=400,
            detail=f"No power plants found for zone '{request.zone_id}'. Create plants first.",
        )

    # Get energy prices - prioritize zone-specific prices, then EIA, then fallback
    price_source = "fallback"

    # 1. Check zone-specific prices first
    if zone.energy_price_usd_mwh is not None:
        marginal_price = zone.energy_price_usd_mwh
        fuel_price = zone.fuel_price_usd_mmbtu or 3.0  # Fuel might not be set
        price_source = f"zone ({zone.slug})"
    else:
        # 2. Try EIA API (use zone's state_code for US regional prices)
        try:
            from src.ingestion.eia_source import EIAClient

            eia_client = EIAClient(api_key=settings.eia_api_key)
            # Use state code for US zones, otherwise national average
            state_for_eia = zone.state_code if zone.country_code == "USA" else None
            prices = eia_client.get_current_prices(state=state_for_eia)
            marginal_price = prices["marginal_price_usd_mwh"]
            fuel_price = prices["fuel_price_usd_mmbtu"]
            price_source = f"eia ({prices['region']})"
        except Exception:
            # 3. Fallback prices
            marginal_price = 100.0
            fuel_price = 3.0
            price_source = "fallback"

    # Calculate SPI projections using scenario builder
    try:
        trend = Trend(snapshot.trend)
    except ValueError:
        trend = Trend.STABLE

    scenario_builder = ScenarioBuilder()

    # Project no-action SPI
    no_action_proj = scenario_builder.build_no_action_scenario(
        current_spi=snapshot.spi_6m,
        trend=trend,
        projection_days=request.projection_days,
    )
    spi_no_action = no_action_proj.ending_spi

    # For with-action, estimate improvement based on action effects
    # Default: assume actions improve SPI by 0.3 on average
    spi_improvement = 0.3
    if request.action_instance_ids:
        from src.db.models import ActionInstance

        total_days_gained = 0
        for aid in request.action_instance_ids:
            try:
                ai = session.query(ActionInstance).filter(ActionInstance.id == UUID(aid)).first()
                if ai and ai.expected_effect:
                    total_days_gained += ai.expected_effect.get("days_gained", 0)
            except ValueError:
                continue
        # Convert days gained to SPI improvement (rough: 1 day ≈ 0.02 SPI)
        spi_improvement = total_days_gained * 0.02

    spi_with_action = min(spi_no_action + spi_improvement, 0.0)  # Cap at 0 (no drought)

    # Calculate economic impact
    calculator = EconomicCostCalculator()
    results = calculator.aggregate_plants(
        plants=plants,
        spi_no_action=spi_no_action,
        spi_with_action=spi_with_action,
        projection_days=request.projection_days,
        marginal_price_usd_mwh=marginal_price,
        fuel_price_usd_mmbtu=fuel_price,
    )

    # Store results in database
    for plant_result in results["per_plant_breakdown"]:
        try:
            plant_id = UUID(plant_result["plant_id"])
            econ_sim = EconomicSimulation(
                power_plant_id=plant_id,
                capacity_loss_pct=plant_result["capacity_loss_no_action"],
                cost_no_action_usd=plant_result["no_action_cost_usd"],
                cost_with_action_usd=plant_result["with_action_cost_usd"],
                savings_usd=plant_result["savings_usd"],
                emergency_fuel_cost_usd=0,  # Could calculate separately
                marginal_price_used=marginal_price,
                fuel_price_used=fuel_price,
                projection_days=request.projection_days,
            )
            session.add(econ_sim)
        except Exception:
            continue

    session.commit()

    # Calculate aggregate scenario results
    total_no_action = results["total_cost_no_action_usd"]
    total_with_action = results["total_cost_with_action_usd"]

    # Average capacity loss
    avg_loss_no_action = (
        sum(p["capacity_loss_no_action"] for p in results["per_plant_breakdown"])
        / len(results["per_plant_breakdown"])
        if results["per_plant_breakdown"]
        else 0
    )
    avg_loss_with_action = (
        sum(p["capacity_loss_with_action"] for p in results["per_plant_breakdown"])
        / len(results["per_plant_breakdown"])
        if results["per_plant_breakdown"]
        else 0
    )

    # Total lost generation
    total_capacity = results["total_capacity_mw"]
    hours = request.projection_days * 24
    lost_gen_no_action = total_capacity * avg_loss_no_action * hours
    lost_gen_with_action = total_capacity * avg_loss_with_action * hours

    # Generate summary
    if results["total_savings_usd"] > 0:
        summary = (
            f"Implementing water actions across {len(plants)} power plants "
            f"({total_capacity:.0f} MW total capacity) "
            f"saves ${results['total_savings_usd']:,.0f} over {request.projection_days} days "
            f"by reducing capacity loss from {avg_loss_no_action:.1%} to {avg_loss_with_action:.1%}."
        )
    else:
        summary = (
            f"Current water stress does not significantly impact the {len(plants)} plants analyzed. "
            f"No immediate economic benefit from water interventions."
        )

    return EconomicSimulationResponse(
        zone_id=zone.slug,
        plants_analyzed=len(plants),
        total_capacity_mw=total_capacity,
        no_action=EconomicScenarioResult(
            capacity_loss_pct=avg_loss_no_action,
            total_cost_usd=total_no_action,
            emergency_fuel_cost_usd=0,
            lost_generation_mwh=lost_gen_no_action,
        ),
        with_action=EconomicScenarioResult(
            capacity_loss_pct=avg_loss_with_action,
            total_cost_usd=total_with_action,
            emergency_fuel_cost_usd=0,
            lost_generation_mwh=lost_gen_with_action,
        ),
        savings_usd=results["total_savings_usd"],
        savings_pct=results["savings_pct"],
        summary=summary,
        per_plant_breakdown=[
            PlantBreakdown(
                plant_id=p["plant_id"],
                plant_name=p["plant_name"],
                capacity_mw=p["capacity_mw"],
                no_action_cost_usd=p["no_action_cost_usd"],
                with_action_cost_usd=p["with_action_cost_usd"],
                savings_usd=p["savings_usd"],
                capacity_loss_no_action=p["capacity_loss_no_action"],
                capacity_loss_with_action=p["capacity_loss_with_action"],
            )
            for p in results["per_plant_breakdown"]
        ],
        marginal_price_used_usd_mwh=marginal_price,
        fuel_price_used_usd_mmbtu=fuel_price,
        projection_days=request.projection_days,
        calculated_at=results["calculated_at"],
    )


@router.get("/prices/history", response_model=EnergyPriceHistoryResponse)
def get_price_history(
    region: str = Query("US", description="Region code"),
    price_type: str = Query("electricity", description="electricity or fuel"),
    days: int = Query(30, ge=1, le=365, description="Days of history"),
):
    """
    Get historical energy prices for trend analysis.
    """
    settings = get_settings()

    if not settings.eia_api_key:
        return EnergyPriceHistoryResponse(
            region=region,
            price_type=price_type,
            history=[],
            total=0,
        )

    try:
        from src.ingestion.eia_source import EIAClient

        client = EIAClient(api_key=settings.eia_api_key)

        if price_type == "electricity":
            df = client.fetch_electricity_prices(state=region if region != "US" else None)
            history = [
                EnergyPriceHistoryPoint(
                    period=row.get("period", ""),
                    price_usd_mwh=row.get("price_usd_mwh"),
                )
                for _, row in df.head(days).iterrows()
            ]
        else:
            df = client.fetch_natural_gas_prices()
            history = [
                EnergyPriceHistoryPoint(
                    period=row.get("period", ""),
                    price_usd_mmbtu=row.get("price_usd_mmbtu"),
                )
                for _, row in df.head(days).iterrows()
            ]

        return EnergyPriceHistoryResponse(
            region=region,
            price_type=price_type,
            history=history,
            total=len(history),
        )
    except Exception as e:
        return EnergyPriceHistoryResponse(
            region=region,
            price_type=price_type,
            history=[],
            total=0,
        )
