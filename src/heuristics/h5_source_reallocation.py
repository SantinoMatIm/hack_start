"""H5: Source Reallocation Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H5SourceReallocation(BaseHeuristic):
    """
    H5: Emergency Source Reallocation

    Activation: SPI <= -2.0, Trend STABLE/WORSENING, days 15-30
    Impact: 5% supply increase = +5 days

    Emergency water source activation including backup wells,
    tanker deployment, and inter-basin transfers.
    """

    HEURISTIC_ID = "H5"
    SPI_MIN = float("-inf")
    SPI_MAX = -2.0
    DAYS_MIN = 15
    DAYS_MAX = 30
    ALLOWED_TRENDS = (Trend.STABLE, Trend.WORSENING)
    APPLICABLE_ACTION_CODES = [
        "H5_EMERGENCY_WELLS",
        "H5_TANKER_DEPLOYMENT",
        "H5_INTERBASIN_TRANSFER",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for source reallocation.

        Very high priority due to critical SPI and limited time.
        """
        # Base priority - emergency measures are highest priority
        base = 80 + (abs(context.spi) - 2.0) * 10  # 80-100 range

        # Trend adjustment
        if context.trend == Trend.WORSENING:
            base += 5
        # STABLE trend still urgent at this SPI level

        # Profile adjustment
        if context.profile == Profile.GOVERNMENT:
            base += 5  # Government coordinates emergency supply
        else:
            base += 5

        # Days to critical
        if context.days_to_critical:
            if context.days_to_critical < 20:
                base += 10
            elif context.days_to_critical < 25:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for source reallocation actions."""
        days_str = (
            f"{context.days_to_critical} days"
            if context.days_to_critical
            else "critical timeline"
        )

        trend_note = (
            "and continuing to deteriorate"
            if context.trend == Trend.WORSENING
            else "requiring immediate attention"
        )

        return (
            f"[EMERGENCY] SPI-6 = {context.spi:.2f} ({context.risk_level.value}) {trend_note}. "
            f"Only {days_str} remain before critical threshold. "
            f"Emergency water source reallocation required. "
            f"Options: backup wells (+5 days per 5% capacity), tanker deployment (+2 days per 2% supply), "
            f"inter-basin transfer (+10 days per 10% increase, requires coordination)."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters based on urgency and zone."""
        # More aggressive for shorter timelines
        if context.days_to_critical and context.days_to_critical < 20:
            # Maximum emergency response
            return {
                "wells_to_activate": 5,
                "well_extraction_pct": 90,
                "tankers_count": 50,
                "tanker_priority_areas": ["hospitals", "schools", "residential"],
                "interbasin_volume_mld": 200,
                "coordinate_all_sources": True,
            }
        else:
            # Measured emergency response
            return {
                "wells_to_activate": 3,
                "well_extraction_pct": 75,
                "tankers_count": 30,
                "tanker_priority_areas": ["hospitals", "residential"],
                "interbasin_volume_mld": 100,
                "coordinate_all_sources": False,
            }
