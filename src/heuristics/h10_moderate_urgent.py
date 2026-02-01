"""H10: Moderate Urgent - SPI bad, medium runway."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H10ModerateUrgent(BaseHeuristic):
    """
    H10: Moderate Urgent

    Activation: SPI -1.5 to -1.0, days 15-55, WORSENING
    Covers: Moderate-severe drought with 2-8 weeks runway.
    """

    HEURISTIC_ID = "H10"
    SPI_MIN = -1.5
    SPI_MAX = -1.0
    DAYS_MIN = 15
    DAYS_MAX = 55
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = [
        "H3_AWARENESS_CAMPAIGN",
        "H2_PRESSURE_REDUCTION",
        "H1_INDUSTRIAL_AUDIT",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 55 + (abs(context.spi) - 1.0) * 20
        if context.days_to_critical and context.days_to_critical < 30:
            base += 10
        if context.profile == Profile.INDUSTRY:
            base += 8
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        days_str = f"{context.days_to_critical} days" if context.days_to_critical else "weeks"
        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), worsening, {days_str} to critical. "
            f"Moderate-urgent: combine awareness, pressure management, and industrial audit. "
            f"Target 5-8% demand reduction to extend supply timeline."
        )
