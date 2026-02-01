"""H14: Improving Maintenance - recovery phase."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H14ImprovingMaintenance(BaseHeuristic):
    """
    H14: Improving Maintenance

    Activation: SPI -1.5 to -0.5, IMPROVING
    Covers: Conditions improving - maintain light measures, avoid premature relaxation.
    """

    HEURISTIC_ID = "H14"
    SPI_MIN = -1.5
    SPI_MAX = -0.5
    DAYS_MIN = None
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.IMPROVING,)
    APPLICABLE_ACTION_CODES = ["H3_AWARENESS_CAMPAIGN", "H3_HOTLINE_LAUNCH"]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 30 + abs(context.spi) * 10
        if context.spi < -1.0:
            base += 10  # Still quite dry
        if context.profile == Profile.GOVERNMENT:
            base += 5
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        return (
            f"SPI-6 = {context.spi:.2f}, trend improving. Recovery phase: "
            f"Maintain awareness and hotline to consolidate conservation gains. "
            f"Avoid relaxing measures too soon; gradual normalization recommended."
        )
