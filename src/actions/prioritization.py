"""Action prioritization engine based on profile weights."""

from typing import Optional
from dataclasses import dataclass
import uuid

from sqlalchemy.orm import Session

from src.config.constants import Profile, PROFILE_WEIGHTS, RiskLevel, Trend
from src.db.models import Action, ActionInstance
from src.actions.action_catalog import ActionCatalog


@dataclass
class PrioritizedAction:
    """A prioritized action with calculated score."""

    action: Action
    priority_score: float
    heuristic_score: float
    profile_adjustment: float
    urgency_adjustment: float
    parameters: dict
    justification: str
    expected_effect: dict


class ActionPrioritizer:
    """
    Prioritize actions based on profile weights and context.

    Different profiles (Government, Industry) weight actions differently:
    - Government: Prioritizes public health, equity, implementation speed
    - Industry: Prioritizes economic impact, implementation speed
    """

    def __init__(self, session: Session):
        self.session = session
        self.catalog = ActionCatalog(session)

    def calculate_action_score(
        self,
        action: Action,
        profile: Profile,
        heuristic_priority: float,
        spi: float,
        days_to_critical: Optional[int],
    ) -> tuple[float, dict]:
        """
        Calculate priority score for an action.

        Args:
            action: Base action
            profile: User profile
            heuristic_priority: Priority from heuristic evaluation
            spi: Current SPI value
            days_to_critical: Days until critical threshold

        Returns:
            Tuple of (total_score, score_breakdown)
        """
        weights = PROFILE_WEIGHTS[profile]

        # Start with heuristic priority (0-100)
        base_score = heuristic_priority

        # Calculate factor scores based on action characteristics
        factors = self._estimate_action_factors(action, spi, days_to_critical)

        # Apply profile weights
        weighted_factors = 0
        for factor, value in factors.items():
            weight = weights.get(factor, 1.0)
            weighted_factors += value * weight

        # Normalize weighted factors to 0-20 range
        max_weighted = sum(weights.values()) * 10
        factor_adjustment = (weighted_factors / max_weighted) * 20

        # Urgency adjustment based on days to critical
        urgency_adjustment = 0
        if days_to_critical is not None:
            if days_to_critical < 15:
                urgency_adjustment = 15
            elif days_to_critical < 30:
                urgency_adjustment = 10
            elif days_to_critical < 45:
                urgency_adjustment = 5

        total_score = base_score + factor_adjustment + urgency_adjustment

        breakdown = {
            "base_heuristic_score": base_score,
            "profile_adjustment": factor_adjustment,
            "urgency_adjustment": urgency_adjustment,
            "factors": factors,
        }

        return min(100, total_score), breakdown

    def _estimate_action_factors(
        self,
        action: Action,
        spi: float,
        days_to_critical: Optional[int],
    ) -> dict:
        """
        Estimate factor scores for an action.

        Factors:
        - public_health: Impact on public health (0-10)
        - economic_impact: Economic cost/benefit (0-10)
        - implementation_speed: How quickly it can be implemented (0-10)
        - political_feasibility: Political acceptability (0-10)
        - equity: Fairness across population (0-10)
        """
        heuristic = action.heuristic

        # Default factor estimates by heuristic type
        factor_profiles = {
            "H1": {  # Industrial reduction
                "public_health": 5,
                "economic_impact": 3,
                "implementation_speed": 6,
                "political_feasibility": 7,
                "equity": 8,
            },
            "H2": {  # Pressure management
                "public_health": 7,
                "economic_impact": 6,
                "implementation_speed": 7,
                "political_feasibility": 8,
                "equity": 9,
            },
            "H3": {  # Public communication
                "public_health": 6,
                "economic_impact": 8,
                "implementation_speed": 9,
                "political_feasibility": 9,
                "equity": 9,
            },
            "H4": {  # Non-essential restriction
                "public_health": 8,
                "economic_impact": 5,
                "implementation_speed": 8,
                "political_feasibility": 5,
                "equity": 6,
            },
            "H5": {  # Source reallocation
                "public_health": 9,
                "economic_impact": 4,
                "implementation_speed": 5,
                "political_feasibility": 6,
                "equity": 7,
            },
            "H6": {  # Emergency escalation
                "public_health": 10,
                "economic_impact": 3,
                "implementation_speed": 6,
                "political_feasibility": 5,
                "equity": 7,
            },
        }

        return factor_profiles.get(heuristic, {
            "public_health": 5,
            "economic_impact": 5,
            "implementation_speed": 5,
            "political_feasibility": 5,
            "equity": 5,
        })

    def prioritize_actions(
        self,
        recommendations: list[dict],
        profile: Profile,
        spi: float,
        days_to_critical: Optional[int],
    ) -> list[PrioritizedAction]:
        """
        Prioritize a list of recommended actions.

        Args:
            recommendations: List of action recommendations from heuristics
            profile: User profile
            spi: Current SPI value
            days_to_critical: Days to critical

        Returns:
            List of PrioritizedAction sorted by priority
        """
        prioritized = []

        for rec in recommendations:
            action = self.catalog.get_action_by_code(rec["action_code"])
            if not action:
                continue

            heuristic_priority = rec.get("priority_score", 50)

            score, breakdown = self.calculate_action_score(
                action=action,
                profile=profile,
                heuristic_priority=heuristic_priority,
                spi=spi,
                days_to_critical=days_to_critical,
            )

            # Estimate expected effect
            expected_effect = self._estimate_effect(action, rec.get("default_parameters", {}))

            prioritized_action = PrioritizedAction(
                action=action,
                priority_score=score,
                heuristic_score=breakdown["base_heuristic_score"],
                profile_adjustment=breakdown["profile_adjustment"],
                urgency_adjustment=breakdown["urgency_adjustment"],
                parameters=rec.get("default_parameters", {}),
                justification=rec.get("justification", ""),
                expected_effect=expected_effect,
            )

            prioritized.append(prioritized_action)

        # Sort by priority score
        prioritized.sort(key=lambda p: p.priority_score, reverse=True)

        return prioritized

    def _estimate_effect(self, action: Action, parameters: dict) -> dict:
        """
        Estimate the effect of an action based on its impact formula.

        Parses formulas like "5% reduction = +3 days" to estimate days gained.
        """
        # Simple parsing of impact formulas
        formula = action.impact_formula.lower()

        # Try to extract days from formula
        days_gained = 0

        if "days" in formula:
            # Extract number before "days"
            import re
            match = re.search(r'[+]?(\d+(?:\.\d+)?)\s*days', formula)
            if match:
                days_gained = float(match.group(1))

        return {
            "days_gained": days_gained,
            "formula": action.impact_formula,
            "confidence": "estimated",
        }

    def create_action_instance(
        self,
        zone_id: uuid.UUID,
        prioritized_action: PrioritizedAction,
        profile: Profile,
    ) -> ActionInstance:
        """
        Create an action instance from a prioritized action.

        Args:
            zone_id: Zone UUID
            prioritized_action: Prioritized action to instantiate
            profile: User profile

        Returns:
            Created ActionInstance (not committed)
        """
        instance = ActionInstance(
            zone_id=zone_id,
            base_action_id=prioritized_action.action.id,
            profile=profile.value,
            parameters=prioritized_action.parameters,
            justification=prioritized_action.justification,
            expected_effect=prioritized_action.expected_effect,
            priority_score=prioritized_action.priority_score,
        )

        return instance
