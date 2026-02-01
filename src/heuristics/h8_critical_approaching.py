"""H8: Critical Approaching Heuristic - fills gap for Texas-like cases."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H8CriticalApproaching(BaseHeuristic):
    """
    H8: Critical Approaching (Texas-like case)

    Activation: SPI -1.8 to -1.5, days < 35, WORSENING
    Covers: High/critical risk with short runway, not yet at H4 threshold.

    Actions: Restrictions + pressure + awareness.
    """

    HEURISTIC_ID = "H8"
    SPI_MIN = -1.85
    SPI_MAX = -1.5
    DAYS_MIN = None
    DAYS_MAX = 35
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = [
        "H4_LAWN_BAN",
        "H3_AWARENESS_CAMPAIGN",
        "H2_PRESSURE_REDUCTION",
        "H2_LEAK_DETECTION",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """Higher priority when closer to critical."""
        base = 75 + (abs(context.spi) - 1.5) * 15
        if context.days_to_critical and context.days_to_critical < 15:
            base += 15
        elif context.days_to_critical and context.days_to_critical < 25:
            base += 8
        if context.profile == Profile.GOVERNMENT:
            base += 5
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        days_str = f"{context.days_to_critical} days" if context.days_to_critical else "limited time"
        return (
            f"[URGENT] SPI-6 = {context.spi:.2f} ({context.risk_level.value}), worsening, {days_str} to critical. "
            f"Conditions approaching critical threshold. Implement restrictions and pressure management now to extend supply. "
            f"Lawn limits, leak detection, and awareness can add 5-15 days buffer."
        )
