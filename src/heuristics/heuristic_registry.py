"""Heuristic registry for coordinating all heuristic rules."""

from typing import Optional
from sqlalchemy.orm import Session

from src.config.constants import RiskLevel, Trend, Profile
from src.db.models import Zone, Action
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext, HeuristicResult
from src.heuristics.h1_industrial_reduction import H1IndustrialReduction
from src.heuristics.h2_pressure_management import H2PressureManagement
from src.heuristics.h3_public_communication import H3PublicCommunication
from src.heuristics.h4_nonessential_restriction import H4NonessentialRestriction
from src.heuristics.h5_source_reallocation import H5SourceReallocation
from src.heuristics.h6_severity_escalation import H6SeverityEscalation
from src.heuristics.h7_preventive_monitoring import H7PreventiveMonitoring


class HeuristicRegistry:
    """
    Registry for all heuristic rules.

    Coordinates evaluation of all heuristics and aggregates results.
    """

    def __init__(self, session: Optional[Session] = None):
        self.session = session
        self._heuristics: list[BaseHeuristic] = [
            H1IndustrialReduction(),
            H2PressureManagement(),
            H3PublicCommunication(),
            H4NonessentialRestriction(),
            H5SourceReallocation(),
            H6SeverityEscalation(),
            H7PreventiveMonitoring(),
        ]

    def get_heuristic(self, heuristic_id: str) -> Optional[BaseHeuristic]:
        """Get a specific heuristic by ID."""
        for h in self._heuristics:
            if h.heuristic_id == heuristic_id:
                return h
        return None

    def evaluate_all(self, context: HeuristicContext) -> list[HeuristicResult]:
        """
        Evaluate all heuristics and return activated ones.

        Args:
            context: Current risk context

        Returns:
            List of HeuristicResults for activated heuristics
        """
        results = []

        for heuristic in self._heuristics:
            result = heuristic.evaluate(context)
            if result.activated:
                results.append(result)

        # Sort by priority (highest first)
        results.sort(key=lambda r: r.priority_score, reverse=True)

        return results

    def build_context(
        self,
        spi: float,
        risk_level: RiskLevel,
        trend: Trend,
        days_to_critical: Optional[int],
        profile: Profile,
        zone_slug: str,
        rapid_deterioration: bool = False,
        recent_spi_change: Optional[float] = None,
    ) -> HeuristicContext:
        """
        Build a HeuristicContext from individual parameters.

        Args:
            spi: Current SPI-6 value
            risk_level: Current risk level
            trend: Current trend
            days_to_critical: Estimated days to critical
            profile: User profile (government/industry)
            zone_slug: Zone identifier
            rapid_deterioration: Whether rapid deterioration detected
            recent_spi_change: Recent SPI change value

        Returns:
            HeuristicContext instance
        """
        return HeuristicContext(
            spi=spi,
            risk_level=risk_level,
            trend=trend,
            days_to_critical=days_to_critical,
            profile=profile,
            zone_slug=zone_slug,
            rapid_deterioration=rapid_deterioration,
            recent_spi_change=recent_spi_change,
        )

    def get_applicable_actions(
        self,
        results: list[HeuristicResult],
    ) -> list[str]:
        """
        Get all unique action codes from activated heuristics.

        Args:
            results: List of activated heuristic results

        Returns:
            List of unique action codes
        """
        action_codes = set()
        for result in results:
            action_codes.update(result.applicable_actions)
        return list(action_codes)

    def get_actions_from_db(
        self,
        action_codes: list[str],
    ) -> list[Action]:
        """
        Fetch action details from database.

        Args:
            action_codes: List of action codes to fetch

        Returns:
            List of Action model instances
        """
        if not self.session or not action_codes:
            return []

        return (
            self.session.query(Action)
            .filter(Action.code.in_(action_codes))
            .all()
        )

    def get_recommended_actions(
        self,
        context: HeuristicContext,
    ) -> dict:
        """
        Get recommended actions for a given context.

        Evaluates all heuristics, collects applicable actions,
        and returns prioritized recommendations.

        Args:
            context: Current risk context

        Returns:
            Dictionary with activated heuristics and recommended actions
        """
        # Evaluate all heuristics
        results = self.evaluate_all(context)

        # Get unique action codes
        action_codes = self.get_applicable_actions(results)

        # Fetch action details if session available
        actions = self.get_actions_from_db(action_codes)
        actions_by_code = {a.code: a for a in actions}

        # Build recommendations
        recommendations = []

        for result in results:
            for action_code in result.applicable_actions:
                action = actions_by_code.get(action_code)

                recommendation = {
                    "action_code": action_code,
                    "heuristic_id": result.heuristic_id,
                    "priority_score": result.priority_score,
                    "justification": result.justification,
                    "default_parameters": result.parameters,
                }

                if action:
                    recommendation.update({
                        "title": action.title,
                        "description": action.description,
                        "impact_formula": action.impact_formula,
                        "default_urgency_days": action.default_urgency_days,
                        "parameter_schema": action.parameter_schema,
                    })

                recommendations.append(recommendation)

        # Sort by priority
        recommendations.sort(key=lambda r: r["priority_score"], reverse=True)

        return {
            "context": {
                "spi": context.spi,
                "risk_level": context.risk_level.value,
                "trend": context.trend.value,
                "days_to_critical": context.days_to_critical,
                "profile": context.profile.value,
                "zone": context.zone_slug,
            },
            "activated_heuristics": [
                {
                    "id": r.heuristic_id,
                    "priority": r.priority_score,
                    "actions_count": len(r.applicable_actions),
                }
                for r in results
            ],
            "recommendations": recommendations,
        }
