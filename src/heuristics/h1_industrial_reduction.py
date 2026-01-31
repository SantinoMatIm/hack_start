"""H1: Industrial Reduction Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H1IndustrialReduction(BaseHeuristic):
    """
    H1: Industrial Water Reduction

    Activation: SPI -1.5 to -1.0, Trend STABLE/WORSENING, days > 45
    Impact: 5% reduction = +3 days

    Targets industrial facilities for water efficiency measures.
    """

    HEURISTIC_ID = "H1"
    SPI_MIN = -1.5
    SPI_MAX = -1.0
    DAYS_MIN = 45
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.STABLE, Trend.WORSENING)
    APPLICABLE_ACTION_CODES = ["H1_INDUSTRIAL_AUDIT", "H1_RECYCLING_MANDATE"]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority based on SPI severity and profile.

        Industrial actions have higher priority for industry profile.
        """
        # Base priority from SPI severity (more negative = higher priority)
        base = 50 + (abs(context.spi) - 1.0) * 20  # 50-60 range

        # Trend adjustment
        if context.trend == Trend.WORSENING:
            base += 10

        # Profile adjustment
        if context.profile == Profile.INDUSTRY:
            base += 15  # Industry cares more about industrial measures
        else:
            base += 5

        # Days to critical adjustment
        if context.days_to_critical and context.days_to_critical < 60:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for industrial reduction actions."""
        trend_str = "improving" if context.trend == Trend.IMPROVING else (
            "worsening" if context.trend == Trend.WORSENING else "stable"
        )

        days_str = (
            f"with {context.days_to_critical} days to critical"
            if context.days_to_critical
            else ""
        )

        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), {trend_str} {days_str}. "
            f"Industrial water reduction recommended as proactive measure. "
            f"Target: 5-10% reduction in industrial consumption for +3-6 days buffer."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters based on severity."""
        # More aggressive for worse conditions
        if context.spi < -1.3:
            reduction_target = 10
            threshold = 8000
        else:
            reduction_target = 5
            threshold = 10000

        return {
            "reduction_target_pct": reduction_target,
            "facility_threshold_m3": threshold,
            "sectors": ["manufacturing", "food_processing"],
        }
