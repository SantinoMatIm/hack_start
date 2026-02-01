"""H12: Stable Severe - bad SPI but not worsening."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H12StableSevere(BaseHeuristic):
    """
    H12: Stable Severe

    Activation: SPI -2.0 to -1.2, STABLE
    Covers: Severe drought holding steady - maintain vigilance, avoid complacency.
    """

    HEURISTIC_ID = "H12"
    SPI_MIN = -2.0
    SPI_MAX = -1.2
    DAYS_MIN = None
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.STABLE,)
    APPLICABLE_ACTION_CODES = [
        "H3_AWARENESS_CAMPAIGN",
        "H2_PRESSURE_REDUCTION",
        "H2_LEAK_DETECTION",
        "H4_LAWN_BAN",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 50 + (abs(context.spi) - 1.2) * 15
        if context.profile == Profile.GOVERNMENT:
            base += 8
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), stable (not worsening). "
            f"Conditions severe but holding. Maintain restrictions and pressure management to prevent relapse. "
            f"Do not relax measures; stable can shift to worsening quickly."
        )
