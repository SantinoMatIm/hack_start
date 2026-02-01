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
    AIBrief,
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
        state = region if region and region != "US" else None
        prices = client.get_current_prices(state=state)

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

    from src.db.retry import get_session_with_retry
    from src.db.models import Zone, PowerPlant, RiskSnapshot, EconomicSimulation
    from src.economic.cost_calculator import EconomicCostCalculator
    from src.simulation.scenario_builder import ScenarioBuilder
    from src.config.constants import Trend

    session = get_session_with_retry()
    
    try:
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
        total_days_gained = 0
        
        if request.action_instance_ids:
            from src.db.models import ActionInstance

            for aid in request.action_instance_ids:
                try:
                    ai = session.query(ActionInstance).filter(ActionInstance.id == UUID(aid)).first()
                    if ai and ai.expected_effect:
                        days = ai.expected_effect.get("days_gained", 0)
                        total_days_gained += days
                except ValueError:
                    continue
            
            if total_days_gained > 0:
                # Convert days gained to SPI improvement
                # More aggressive factor: 1 day ≈ 0.05 SPI (was 0.02, too conservative)
                spi_improvement = total_days_gained * 0.05
        
        # Build with-action trajectory by applying SPI improvement to each day
        # The improvement ramps up over the first 14 days (action implementation time)
        spi_trajectory_with_action = []
        for point in no_action_proj.trajectory:
            day = point.get("day", 0)
            base_spi = point.get("projected_spi", snapshot.spi_6m)
            
            # Ramp up improvement over first 14 days
            ramp_factor = min(1.0, day / 14.0) if day > 0 else 0
            day_improvement = spi_improvement * ramp_factor
            
            improved_spi = min(base_spi + day_improvement, 0.0)  # Cap at 0
            spi_trajectory_with_action.append({
                "day": day,
                "projected_spi": improved_spi,
            })
        
        # Calculate average SPI for summary reporting
        def calculate_weighted_avg_spi(trajectory: list) -> float:
            """Calculate time-weighted average SPI over projection."""
            if not trajectory:
                return snapshot.spi_6m
            total = sum(p.get("projected_spi", snapshot.spi_6m) for p in trajectory)
            return total / len(trajectory)
        
        spi_no_action_avg = calculate_weighted_avg_spi(no_action_proj.trajectory)
        spi_with_action_avg = calculate_weighted_avg_spi(spi_trajectory_with_action)

        # Calculate economic impact using day-by-day trajectory
        calculator = EconomicCostCalculator()
        results = calculator.aggregate_plants(
            plants=plants,
            spi_no_action=spi_no_action_avg,
            spi_with_action=spi_with_action_avg,
            projection_days=request.projection_days,
            marginal_price_usd_mwh=marginal_price,
            fuel_price_usd_mmbtu=fuel_price,
            spi_trajectory_no_action=no_action_proj.trajectory,
            spi_trajectory_with_action=spi_trajectory_with_action,
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

        # Calculate effective capacity loss from actual costs
        # This reflects the day-by-day calculation more accurately
        total_capacity = results["total_capacity_mw"]
        hours = request.projection_days * 24
        
        # Maximum possible cost if 100% capacity was lost
        max_possible_cost = total_capacity * hours * marginal_price
        
        # Effective capacity loss = actual_cost / max_possible_cost
        effective_loss_no_action = (
            total_no_action / max_possible_cost
            if max_possible_cost > 0
            else 0
        )
        effective_loss_with_action = (
            total_with_action / max_possible_cost
            if max_possible_cost > 0
            else 0
        )

        # Total lost generation based on effective loss
        lost_gen_no_action = total_capacity * effective_loss_no_action * hours
        lost_gen_with_action = total_capacity * effective_loss_with_action * hours

        # Generate summary
        if results["total_savings_usd"] > 0:
            # Calculate effective cost reduction percentage
            cost_reduction_pct = (results["total_savings_usd"] / total_no_action * 100) if total_no_action > 0 else 0
            summary = (
                f"Implementing water actions across {len(plants)} power plants "
                f"({total_capacity:.0f} MW total capacity) "
                f"saves ${results['total_savings_usd']:,.0f} over {request.projection_days} days "
                f"({cost_reduction_pct:.1f}% cost reduction) by delaying critical drought impacts."
            )
        else:
            summary = (
                f"Current water stress does not significantly impact the {len(plants)} plants analyzed. "
                f"No immediate economic benefit from water interventions."
            )

        # Generate AI brief (optional - only if OpenAI key is configured)
        ai_brief = None
        try:
            from src.ai_orchestrator.brief_generator import generate_ai_brief, get_fallback_brief
            from src.db.models import Action, ActionInstance
            
            # Get action names for the brief
            action_names = []
            if request.action_instance_ids:
                for aid in request.action_instance_ids:
                    try:
                        ai = session.query(ActionInstance).filter(ActionInstance.id == UUID(aid)).first()
                        if ai:
                            action = session.query(Action).filter(Action.id == ai.base_action_id).first()
                            if action:
                                action_names.append(action.title)
                    except ValueError:
                        continue
            
            # Get plant types
            plant_types = [p.plant_type for p in plants]
            
            # Try AI generation first
            brief_data = generate_ai_brief(
                zone_id=zone.slug,
                spi=snapshot.spi_6m,
                risk_level=snapshot.risk_level,
                trend=snapshot.trend,
                days_to_critical=snapshot.days_to_critical,
                plants_count=len(plants),
                total_capacity_mw=total_capacity,
                plant_types=plant_types,
                projection_days=request.projection_days,
                no_action_cost=total_no_action,
                no_action_loss=effective_loss_no_action,
                with_action_cost=total_with_action,
                with_action_loss=effective_loss_with_action,
                savings=results["total_savings_usd"],
                savings_pct=results["savings_pct"],
                actions=action_names,
            )
            
            # Use fallback if AI generation fails
            if not brief_data:
                brief_data = get_fallback_brief(
                    savings=results["total_savings_usd"],
                    savings_pct=results["savings_pct"],
                    risk_level=snapshot.risk_level,
                    projection_days=request.projection_days,
                    actions=action_names,
                )
                ai_brief = AIBrief(
                    executive_summary=brief_data["executive_summary"],
                    risk_context=brief_data["risk_context"],
                    action_rationale=brief_data["action_rationale"],
                    recommendation=brief_data["recommendation"],
                    generated=False,  # Mark as fallback
                )
            else:
                ai_brief = AIBrief(
                    executive_summary=brief_data["executive_summary"],
                    risk_context=brief_data["risk_context"],
                    action_rationale=brief_data["action_rationale"],
                    recommendation=brief_data["recommendation"],
                    generated=True,
                )
        except Exception as e:
            print(f"Failed to generate AI brief: {e}")
            # Continue without AI brief

        return EconomicSimulationResponse(
            zone_id=zone.slug,
            plants_analyzed=len(plants),
            total_capacity_mw=total_capacity,
            no_action=EconomicScenarioResult(
                capacity_loss_pct=effective_loss_no_action,
                total_cost_usd=total_no_action,
                emergency_fuel_cost_usd=0,
                lost_generation_mwh=lost_gen_no_action,
            ),
            with_action=EconomicScenarioResult(
                capacity_loss_pct=effective_loss_with_action,
                total_cost_usd=total_with_action,
                emergency_fuel_cost_usd=0,
                lost_generation_mwh=lost_gen_with_action,
            ),
            savings_usd=results["total_savings_usd"],
            savings_pct=results["savings_pct"],
            summary=summary,
            ai_brief=ai_brief,
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
    finally:
        session.close()


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
