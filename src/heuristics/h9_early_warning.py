"""H9: Early Warning Heuristic - mild dry, worsening."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H9EarlyWarning(BaseHeuristic):
    """
    H9: Early Warning

    Activation: SPI -0.8 to -0.3, WORSENING
    Covers: Mild drought, trend worsening - proactive preparedness.
    """

    HEURISTIC_ID = "H9"
    SPI_MIN = -0.8
    SPI_MAX = -0.3
    DAYS_MIN = None
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = ["H3_AWARENESS_CAMPAIGN", "H3_HOTLINE_LAUNCH"]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 35 + abs(context.spi) * 15
        if context.profile == Profile.GOVERNMENT:
            base += 10
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        return (
            f"SPI-6 = {context.spi:.2f} (mild dry), worsening trend. Early warning: "
            f"Launch awareness campaign and hotline to build conservation habits before conditions deteriorate. "
            f"Proactive measures reduce peak demand when drought intensifies."
        )
