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
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            zone_id = request.zone_id.lower()
            demo_risk = {
                "cdmx": {"spi": -1.72, "risk_level": "HIGH", "trend": "WORSENING", "days_to_critical": 24},
                "monterrey": {"spi": -1.45, "risk_level": "HIGH", "trend": "STABLE", "days_to_critical": 38},
            }

            if zone_id not in demo_risk:
                raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

            risk = demo_risk[zone_id]
            current_spi = risk["spi"]
            days_to_critical = risk["days_to_critical"]

            # Generate demo trajectory
            projection_days = request.projection_days
            no_action_trajectory = []
            with_action_trajectory = []

            for day in range(0, projection_days + 1, 10):
                # No action: SPI decreases
                no_action_spi = current_spi - (0.02 * day)
                no_action_trajectory.append(TrajectoryPoint(day=day, spi=round(no_action_spi, 2)))

                # With action: SPI decreases slower
                with_action_spi = current_spi - (0.008 * day)
                with_action_trajectory.append(TrajectoryPoint(day=day, spi=round(with_action_spi, 2)))

            return SimulationResponse(
                zone_id=zone_id,
                no_action=ScenarioResult(
                    ending_spi=round(current_spi - 0.4, 2),
                    ending_risk_level="CRITICAL",
                    days_to_critical=days_to_critical,
                    trajectory=no_action_trajectory,
                ),
                with_action=ScenarioResult(
                    ending_spi=round(current_spi - 0.15, 2),
                    ending_risk_level="HIGH",
                    days_to_critical=days_to_critical + 28,
                    trajectory=with_action_trajectory,
                ),
                comparison=ScenarioComparison(
                    days_gained=28,
                    spi_improvement=0.25,
                    risk_level_change="CRITICAL → HIGH",
                    actions_count=len(request.action_codes) if request.action_codes else 3,
                ),
                summary=f"Implementing the recommended actions extends the time to critical threshold by 28 days, improving projected conditions from CRITICAL to HIGH risk level.",
            )
    except HTTPException:
        raise
    except Exception:
        pass

    # Full database mode
    import re
    from src.db.connection import get_session
    from src.db.models import Zone, RiskSnapshot, Action
    from src.simulation.delta_calculator import DeltaCalculator

    session = next(get_session())

    # Get zone
    zone = session.query(Zone).filter(Zone.slug == request.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

    # Get latest risk snapshot
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

    # Get actions
    actions_data = []
    for code in request.action_codes:
        action = session.query(Action).filter(Action.code == code).first()
        if action:
            days_match = re.search(
                r'[+]?(\d+(?:\.\d+)?)\s*days',
                action.impact_formula.lower(),
            )
            days_gained = float(days_match.group(1)) if days_match else 0

            actions_data.append({
                "action_code": action.code,
                "title": action.title,
                "impact_formula": action.impact_formula,
                "urgency_days": action.default_urgency_days,
                "expected_effect": {
                    "days_gained": days_gained,
                    "confidence": "estimated",
                },
            })

    if not actions_data:
        raise HTTPException(
            status_code=400,
            detail="No valid actions found for the provided codes.",
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
    )
