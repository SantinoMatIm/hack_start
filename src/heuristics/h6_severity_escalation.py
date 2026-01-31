"""H6: Severity Escalation Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H6SeverityEscalation(BaseHeuristic):
    """
    H6: Severity Escalation / Emergency Declaration

    Activation: SPI threshold crossed OR rapid deterioration (>20% in 2 weeks)
    Impact: Combined effects multiplied by 0.8 (coordination efficiency)

    Triggers formal emergency declaration enabling special powers
    and coordinated multi-action response.
    """

    HEURISTIC_ID = "H6"
    SPI_MIN = float("-inf")
    SPI_MAX = float("inf")
    DAYS_MIN = None
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = ["H6_EMERGENCY_DECLARATION"]

    def check_activation(self, context: HeuristicContext) -> bool:
        """
        Check if escalation should be triggered.

        Activates on:
        1. Rapid deterioration (>20% SPI drop in 2 weeks)
        2. Critical threshold crossing with worsening trend
        """
        # Check trend requirement
        if context.trend != Trend.WORSENING:
            return False

        # Condition 1: Rapid deterioration
        if context.rapid_deterioration:
            return True

        # Condition 2: At or approaching critical with worsening
        if context.spi <= -1.8 and context.days_to_critical and context.days_to_critical < 20:
            return True

        # Condition 3: Already critical
        if context.spi <= -2.0:
            return True

        return False

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for emergency escalation.

        Highest priority when triggered.
        """
        # Base priority - escalation is always high priority when triggered
        base = 85

        # Adjust for severity
        if context.spi <= -2.5:
            base = 100
        elif context.spi <= -2.0:
            base = 95
        elif context.rapid_deterioration:
            base = 90

        # Days to critical
        if context.days_to_critical and context.days_to_critical < 15:
            base = min(100, base + 5)

        return base

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for emergency escalation."""
        triggers = []

        if context.rapid_deterioration:
            triggers.append("rapid deterioration detected (>20% SPI drop)")

        if context.spi <= -2.0:
            triggers.append(f"critical SPI threshold reached ({context.spi:.2f})")

        if context.days_to_critical and context.days_to_critical < 20:
            triggers.append(f"only {context.days_to_critical} days to critical")

        trigger_str = " and ".join(triggers) if triggers else "severe conditions"

        return (
            f"[EMERGENCY ESCALATION] {trigger_str}. "
            f"Formal water emergency declaration recommended to enable coordinated response. "
            f"Emergency powers allow: mandatory rationing, resource requisition, inter-agency coordination. "
            f"Combined action efficiency estimated at 80% of sum of individual effects."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters for emergency declaration."""
        # Determine emergency level
        if context.spi <= -2.5 or (context.days_to_critical and context.days_to_critical < 10):
            level = "level_3"  # Most severe
            duration = 60
        elif context.spi <= -2.0 or (context.days_to_critical and context.days_to_critical < 15):
            level = "level_2"
            duration = 45
        else:
            level = "level_1"
            duration = 30

        return {
            "emergency_level": level,
            "duration_days": duration,
            "enable_rationing": level in ["level_2", "level_3"],
            "enable_requisition": level == "level_3",
            "coordinate_with": ["water_utility", "civil_protection", "health_ministry"],
        }
