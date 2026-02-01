"""Actions router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.config.constants import Profile, RiskLevel, Trend
from src.api.schemas.actions import (
    ActionResponse,
    RecommendedActionsRequest,
    RecommendedActionsResponse,
    RecommendedActionResponse,
    ExpectedEffect,
    ContextSummary,
    ActivatedHeuristic,
)

router = APIRouter(prefix="/actions", tags=["actions"])


# Demo actions data
DEMO_ACTIONS = [
    {
        "id": "demo-1",
        "code": "H4_LAWN_BAN",
        "title": "Lawn/Garden Irrigation Restriction",
        "description": "Restrict lawn and garden irrigation during drought conditions",
        "heuristic": "H4",
        "spi_min": -3.0,
        "spi_max": -1.8,
        "impact_formula": "1% removed → +1.3 days",
        "base_cost": 50000,
        "default_urgency_days": 7,
        "parameter_schema": {"reduction_percentage": {"min": 5, "max": 100}},
    },
    {
        "id": "demo-2",
        "code": "H2_PRESSURE_REDUCTION",
        "title": "Network Pressure Reduction",
        "description": "Reduce water pressure in distribution network during off-peak hours",
        "heuristic": "H2",
        "spi_min": -1.8,
        "spi_max": -1.2,
        "impact_formula": "10% pressure → +4 days",
        "base_cost": 25000,
        "default_urgency_days": 3,
        "parameter_schema": {"pressure_reduction_percent": {"min": 5, "max": 30}},
    },
    {
        "id": "demo-3",
        "code": "H3_AWARENESS_CAMPAIGN",
        "title": "Public Awareness Campaign",
        "description": "Multi-channel public awareness campaign for water conservation",
        "heuristic": "H3",
        "spi_min": -2.0,
        "spi_max": -1.0,
        "impact_formula": "3% reduction → +2 days",
        "base_cost": 75000,
        "default_urgency_days": 14,
        "parameter_schema": {"target_reduction_percent": {"min": 1, "max": 10}},
    },
]


DEMO_RECOMMENDED_ACTIONS = [
    {
        "action_instance_id": "demo-instance-h4-lawn",
        "action_code": "H4_LAWN_BAN",
        "title": "Lawn/Garden Irrigation Restriction",
        "description": "Restrict lawn and garden irrigation during drought conditions",
        "heuristic_id": "H4",
        "priority_score": 85,
        "parameters": {
            "reduction_percentage": 15.0,
            "duration_days": 30,
            "priority_level": "HIGH",
            "enforcement_level": "mandatory"
        },
        "justification": "SPI -1.72, WORSENING trend, 24 days to critical. Non-essential restrictions provide immediate impact.",
        "expected_effect": {"days_gained": 19, "confidence": "estimated", "formula": "1% removed → +1.3 days"},
        "method": "demo"
    },
    {
        "action_instance_id": "demo-instance-h2-pressure",
        "action_code": "H2_PRESSURE_REDUCTION",
        "title": "Network Pressure Reduction",
        "description": "Reduce water pressure in distribution network during off-peak hours",
        "heuristic_id": "H2",
        "priority_score": 78,
        "parameters": {
            "pressure_reduction_percent": 15.0,
            "hours_per_day": 8,
            "priority_level": "HIGH"
        },
        "justification": "SPI in range -1.2 to -1.8, worsening conditions warrant pressure management.",
        "expected_effect": {"days_gained": 6, "confidence": "estimated", "formula": "10% pressure → +4 days"},
        "method": "demo"
    },
    {
        "action_instance_id": "demo-instance-h3-awareness",
        "action_code": "H3_AWARENESS_CAMPAIGN",
        "title": "Public Awareness Campaign",
        "description": "Multi-channel public awareness campaign for water conservation",
        "heuristic_id": "H3",
        "priority_score": 65,
        "parameters": {
            "target_reduction_percent": 5.0,
            "duration_days": 45,
            "priority_level": "MEDIUM",
            "channels": ["social_media", "radio", "billboards"]
        },
        "justification": "SPI below -1.0 with worsening trend. Public communication supports other measures.",
        "expected_effect": {"days_gained": 3, "confidence": "estimated", "formula": "3% reduction → +2 days"},
        "method": "demo"
    }
]


@router.get("", response_model=list[ActionResponse])
def list_actions():
    """
    List all available base actions.

    Returns the full action catalog (15 actions).
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            return [ActionResponse(**a) for a in DEMO_ACTIONS]
    except Exception:
        pass

    # Full database mode
    from src.db.connection import get_session
    from src.actions.action_catalog import ActionCatalog

    session = next(get_session())
    catalog = ActionCatalog(session=session)
    actions = catalog.get_all_actions()

    return [
        ActionResponse(
            id=str(a.id),
            code=a.code,
            title=a.title,
            description=a.description,
            heuristic=a.heuristic,
            spi_min=a.spi_min,
            spi_max=a.spi_max,
            impact_formula=a.impact_formula,
            base_cost=a.base_cost,
            default_urgency_days=a.default_urgency_days,
            parameter_schema=a.parameter_schema,
        )
        for a in actions
    ]


@router.get("/{action_code}", response_model=ActionResponse)
def get_action(action_code: str):
    """
    Get a specific action by code.

    Args:
        action_code: Action code (e.g., 'H1_INDUSTRIAL_AUDIT')
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            for a in DEMO_ACTIONS:
                if a["code"] == action_code:
                    return ActionResponse(**a)
            raise HTTPException(status_code=404, detail=f"Action '{action_code}' not found")
    except HTTPException:
        raise
    except Exception:
        pass

    # Full database mode
    from src.db.connection import get_session
    from src.actions.action_catalog import ActionCatalog

    session = next(get_session())
    catalog = ActionCatalog(session=session)
    action = catalog.get_action_by_code(action_code)

    if not action:
        raise HTTPException(status_code=404, detail=f"Action '{action_code}' not found")

    return ActionResponse(
        id=str(action.id),
        code=action.code,
        title=action.title,
        description=action.description,
        heuristic=action.heuristic,
        spi_min=action.spi_min,
        spi_max=action.spi_max,
        impact_formula=action.impact_formula,
        base_cost=action.base_cost,
        default_urgency_days=action.default_urgency_days,
        parameter_schema=action.parameter_schema,
    )


@router.post("/recommended", response_model=RecommendedActionsResponse)
def get_recommended_actions(
    request: RecommendedActionsRequest,
):
    """
    Get recommended actions based on current risk and profile.

    Evaluates heuristics, selects applicable actions, and parametrizes
    them using AI or fallback logic.

    Args:
        request: Zone ID and user profile
    """
    # Check for demo mode
    try:
        settings = get_settings()
        if settings.is_demo_mode:
            zone_id = request.zone_id.lower()
            profile = request.profile.lower()

            demo_risk = {
                "cdmx": {"spi": -1.72, "risk_level": "HIGH", "trend": "WORSENING", "days_to_critical": 24},
                "monterrey": {"spi": -1.45, "risk_level": "HIGH", "trend": "STABLE", "days_to_critical": 38},
            }

            if zone_id not in demo_risk:
                raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

            risk = demo_risk[zone_id]

            return RecommendedActionsResponse(
                zone_id=zone_id,
                profile=profile,
                context=ContextSummary(
                    spi=risk["spi"],
                    risk_level=risk["risk_level"],
                    trend=risk["trend"],
                    days_to_critical=risk["days_to_critical"],
                    profile=profile,
                    zone=zone_id,
                ),
                activated_heuristics=[
                    ActivatedHeuristic(id="H4", priority=85, actions_count=1),
                    ActivatedHeuristic(id="H2", priority=78, actions_count=1),
                    ActivatedHeuristic(id="H3", priority=65, actions_count=1),
                ],
                actions=[
                    RecommendedActionResponse(
                        action_instance_id=a["action_instance_id"],
                        action_code=a["action_code"],
                        title=a["title"],
                        description=a["description"],
                        heuristic_id=a["heuristic_id"],
                        priority_score=a["priority_score"],
                        parameters=a["parameters"],
                        justification=a["justification"],
                        expected_effect=ExpectedEffect(**a["expected_effect"]),
                        method=a["method"],
                    )
                    for a in DEMO_RECOMMENDED_ACTIONS
                ],
            )
    except HTTPException:
        raise
    except Exception:
        pass

    # Full database mode
    from src.db.connection import get_session
    from src.db.models import Zone, RiskSnapshot, Action, ActionInstance
    from src.heuristics.heuristic_registry import HeuristicRegistry
    from src.ai_orchestrator.orchestrator import AIOrchestrator

    session = next(get_session())

    # Get zone
    zone = session.query(Zone).filter(Zone.slug == request.zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{request.zone_id}' not found")

    # Validate profile
    try:
        profile = Profile(request.profile.lower())
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid profile '{request.profile}'. Use 'government' or 'industry'.",
        )

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
            detail=f"No risk assessment available for zone '{request.zone_id}'. Run risk assessment first.",
        )

    # Build context for heuristics
    registry = HeuristicRegistry(session=session)

    try:
        risk_level = RiskLevel(snapshot.risk_level)
    except ValueError:
        risk_level = RiskLevel.MEDIUM

    try:
        trend = Trend(snapshot.trend)
    except ValueError:
        trend = Trend.STABLE

    context = registry.build_context(
        spi=snapshot.spi_6m,
        risk_level=risk_level,
        trend=trend,
        days_to_critical=snapshot.days_to_critical,
        profile=profile,
        zone_slug=zone.slug,
    )

    # Get recommended actions from heuristics
    recommendations = registry.get_recommended_actions(context)

    # Parametrize actions using AI orchestrator
    ai_orchestrator = AIOrchestrator()

    parameterized_actions = []
    for rec in recommendations["recommendations"]:
        action = session.query(Action).filter(Action.code == rec["action_code"]).first()
        if not action:
            continue

        result = ai_orchestrator.parameterize_action(
            zone=zone.slug,
            spi=snapshot.spi_6m,
            risk_level=risk_level,
            trend=trend,
            days_to_critical=snapshot.days_to_critical,
            profile=profile,
            action_code=action.code,
            action_title=action.title,
            action_description=action.description or "",
            impact_formula=action.impact_formula,
            default_urgency_days=action.default_urgency_days,
            parameter_schema=action.parameter_schema or {},
            default_parameters=rec.get("default_parameters", {}),
        )

        # Persist ActionInstance (OpenAI/fallback parameterization saved to DB)
        action_instance = ActionInstance(
            zone_id=zone.id,
            base_action_id=action.id,
            profile=profile.value,
            parameters=result.parameters,
            justification=result.justification,
            expected_effect=result.expected_effect,
            priority_score=rec.get("priority_score", 50),
        )
        session.add(action_instance)
        session.flush()  # Get action_instance.id for linking in simulations

        parameterized_actions.append(RecommendedActionResponse(
            action_instance_id=str(action_instance.id),
            action_code=result.action_code,
            title=action.title,
            description=action.description,
            heuristic_id=rec.get("heuristic_id", action.heuristic),
            priority_score=rec.get("priority_score", 50),
            parameters=result.parameters,
            justification=result.justification,
            expected_effect=ExpectedEffect(
                days_gained=result.expected_effect.get("days_gained", 0),
                confidence=result.expected_effect.get("confidence", "estimated"),
                formula=action.impact_formula,
            ),
            method=result.method,
        ))

    response = RecommendedActionsResponse(
        zone_id=zone.slug,
        profile=profile.value,
        context=ContextSummary(
            spi=snapshot.spi_6m,
            risk_level=risk_level.value,
            trend=trend.value,
            days_to_critical=snapshot.days_to_critical,
            profile=profile.value,
            zone=zone.slug,
        ),
        activated_heuristics=[
            ActivatedHeuristic(
                id=h["id"],
                priority=h["priority"],
                actions_count=h["actions_count"],
            )
            for h in recommendations["activated_heuristics"]
        ],
        actions=parameterized_actions,
    )
    session.commit()
    return response
