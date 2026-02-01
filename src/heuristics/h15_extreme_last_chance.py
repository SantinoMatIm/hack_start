"""H15: Extreme Last Chance - SPI very low, any trend."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H15ExtremeLastChance(BaseHeuristic):
    """
    H15: Extreme Last Chance

    Activation: SPI <= -2.0, any trend
    Covers: Exceptionally dry - full emergency response regardless of trend.
    """

    HEURISTIC_ID = "H15"
    SPI_MIN = float("-inf")
    SPI_MAX = -2.0
    DAYS_MIN = None
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.STABLE, Trend.WORSENING, Trend.IMPROVING)
    APPLICABLE_ACTION_CODES = [
        "H6_EMERGENCY_DECLARATION",
        "H5_EMERGENCY_WELLS",
        "H5_TANKER_DEPLOYMENT",
        "H4_LAWN_BAN",
        "H4_CARWASH_RESTRICTION",
        "H4_POOL_RESTRICTION",
        "H4_FOUNTAIN_SHUTDOWN",
        "H3_AWARENESS_CAMPAIGN",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        base = 95
        if context.spi < -2.5:
            base = 100
        if context.days_to_critical and context.days_to_critical < 15:
            base = min(100, base + 5)
        return base

    def generate_justification(self, context: HeuristicContext) -> str:
        return (
            f"[EXTREME] SPI-6 = {context.spi:.2f} (exceptionally dry). "
            f"Full emergency response: wells, tankers, all restrictions, emergency declaration. "
            f"Conditions exceed normal thresholds; maximum intervention required."
        )
