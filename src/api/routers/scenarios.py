"""Scenarios/simulation router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.config.constants import Trend
from src.api.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    ScenarioResult,
    ScenarioComparison,
    TrajectoryPoint,
    ActionApplied,
)

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post("/simulate", response_model=SimulationResponse)
def simulate_scenarios(
    request: SimulationRequest,
):
    """
    Simulate act vs. no-act scenarios.

    Compares the projected outcomes with and without the specified actions.

    Args:
        request: Zone ID, action codes, and projection days
    """
    # Simulation requires real data from database
    settings = get_settings()
    if settings.is_demo_mode:
        raise HTTPException(
            status_code=400,
            detail="Simulation requires database. Configure DATABASE_URL and run ingestion to use real zone and risk data.",
        )

    # Database mode - everything from DB
    import uuid as uuid_mod
    from src.db.connection import get_session
    from src.db.models import Zone, RiskSnapshot, ActionInstance
    from src.simulation.delta_calculator import DeltaCalculator

    if not request.action_instance_ids:
        raise HTTPException(
            status_code=400,
            detail="Select at least one action from the Actions page to simulate.",
        )

    session = next(get_session())

    # Get zone (DB)
    zone = session.query(Zone).filter(Zone.slug == request.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

    # Get latest risk snapshot (DB)
    snapshot = (
        session.query(RiskSnapshot)
        .filter(RiskSnapshot.zone_id == zone.id)
        .order_by(RiskSnapshot.created_at.desc())
        .first()
    )
    if not snapshot:
        raise HTTPException(
            status_code=400,
            detail=f"No risk assessment available for zone '{request.zone_id}'.",
        )

    # Fetch ActionInstances by ID (DB only - no impact_formula, no fallback)
    actions_data = []
    actions_applied_list = []

    for ai_id_str in request.action_instance_ids:
        try:
            ai_id = uuid_mod.UUID(ai_id_str)
        except ValueError:
            continue

        ai = (
            session.query(ActionInstance)
            .filter(
                ActionInstance.id == ai_id,
                ActionInstance.zone_id == zone.id,
            )
            .first()
        )
        if not ai or not ai.expected_effect:
            continue

        days_gained = float(ai.expected_effect.get("days_gained", 0) or 0)
        actions_data.append({
            "action_code": ai.base_action.code,
            "action_instance_id": str(ai.id),
            "title": ai.base_action.title,
            "urgency_days": ai.base_action.default_urgency_days,
            "expected_effect": {
                "days_gained": days_gained,
                "confidence": ai.expected_effect.get("confidence", "ai_parameterized"),
            },
        })
        actions_applied_list.append(
            ActionApplied(code=ai.base_action.code, title=ai.base_action.title, days_gained=days_gained)
        )

    if not actions_data:
        raise HTTPException(
            status_code=400,
            detail="No valid ActionInstances found. Get recommended actions from the Actions page first.",
        )

    # Parse trend
    try:
        trend = Trend(snapshot.trend)
    except ValueError:
        trend = Trend.STABLE

    # Run simulation and persist to DB
    calculator = DeltaCalculator(session=session)
    result = calculator.simulate_and_store(
        zone_id=zone.id,
        snapshot_id=snapshot.id,
        current_spi=snapshot.spi_6m,
        trend=trend,
        actions=actions_data,
        projection_days=request.projection_days,
    )

    comparison = result["comparison"]
    no_action = result["no_action"]
    with_action = result["with_action"]

    # Format delta summary
    from src.simulation.scenario_builder import ScenarioBuilder
    builder = ScenarioBuilder()
    no_action_proj = builder.build_no_action_scenario(
        current_spi=snapshot.spi_6m,
        trend=trend,
        projection_days=request.projection_days,
    )
    with_action_proj = builder.build_with_action_scenario(
        current_spi=snapshot.spi_6m,
        trend=trend,
        actions=actions_data,
        projection_days=request.projection_days,
    )
    delta = calculator.calculate_delta(no_action_proj, with_action_proj)
    summary = calculator.format_delta_summary(delta)

    return SimulationResponse(
        zone_id=zone.slug,
        no_action=ScenarioResult(
            ending_spi=no_action["ending_spi"],
            ending_risk_level=no_action["ending_risk_level"],
            days_to_critical=no_action["days_to_critical"],
            trajectory=[
                TrajectoryPoint(
                    day=p.get("day"),
                    projected_spi=p.get("projected_spi"),
                    risk_level=p.get("risk_level"),
                    improvement_applied=p.get("improvement_applied"),
                )
                for p in no_action["trajectory"]
            ],
        ),
        with_action=ScenarioResult(
            ending_spi=with_action["ending_spi"],
            ending_risk_level=with_action["ending_risk_level"],
            days_to_critical=with_action["days_to_critical"],
            trajectory=[
                TrajectoryPoint(
                    day=p.get("day"),
                    projected_spi=p.get("projected_spi"),
                    risk_level=p.get("risk_level"),
                    improvement_applied=p.get("improvement_applied"),
                )
                for p in with_action["trajectory"]
            ],
        ),
        comparison=ScenarioComparison(
            days_gained=int(comparison["days_gained"]),
            spi_improvement=comparison["spi_improvement"],
            risk_level_change=comparison["risk_level_change"],
            actions_count=comparison["actions_count"],
        ),
        summary=summary,
        actions_applied=actions_applied_list,
    )
