"""H11: Short Runway Emergency - very little time left."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H11ShortRunwayEmergency(BaseHeuristic):
    """
    H11: Short Runway Emergency

    Activation: SPI < -1.2, days < 25, WORSENING
    Covers: Severe conditions with under 4 weeks to critical.
    """

    HEURISTIC_ID = "H11"
    SPI_MIN = float("-inf")
    SPI_MAX = -1.2
    DAYS_MIN = None
    DAYS_MAX = 25
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = [
        "H6_EMERGENCY_DECLARATION",
        "H4_LAWN_BAN",
        "H4_CARWASH_RESTRICTION",
        "H3_AWARENESS_CAMPAIGN",
        "H2_PRESSURE_REDUCTION",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 85
        if context.days_to_critical and context.days_to_critical < 15:
            base += 10
        if context.days_to_critical and context.days_to_critical < 7:
            base += 5
        if context.spi < -1.8:
            base += 5
        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        days_str = f"{context.days_to_critical} days" if context.days_to_critical else "< 1 month"
        return (
            f"[EMERGENCY] SPI-6 = {context.spi:.2f}, only {days_str} to critical. "
            f"Short runway: declare emergency, implement all restrictions immediately. "
            f"Lawn, car wash, fountains, pressure reduction, and awareness in parallel."
        )
