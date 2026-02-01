"""H13: Borderline High - approaching high risk."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H13BorderlineHigh(BaseHeuristic):
    """
    H13: Borderline High

    Activation: SPI -1.2 to -0.8, days 20-70, WORSENING
    Covers: Medium-high risk, trend concerning.
    """

    HEURISTIC_ID = "H13"
    SPI_MIN = -1.2
    SPI_MAX = -0.8
    DAYS_MIN = 20
    DAYS_MAX = 70
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = [
        "H3_AWARENESS_CAMPAIGN",
        "H1_INDUSTRIAL_AUDIT",
        "H2_LEAK_DETECTION",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 45 + abs(context.spi) * 15
        if context.days_to_critical and context.days_to_critical < 40:
            base += 8
        if context.profile == Profile.INDUSTRY:
            base += 10
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        return (
            f"SPI-6 = {context.spi:.2f} (borderline high), worsening. "
            f"Conditions approaching high risk. Start industrial audits and leak detection now. "
            f"Awareness campaign to build voluntary conservation before mandatory measures."
        )
