"""H2: Pressure Management Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H2PressureManagement(BaseHeuristic):
    """
    H2: Network Pressure Management

    Activation: SPI -1.8 to -1.2, Trend WORSENING, days 30-45
    Impact: 10% pressure reduction = +4 days

    Targets water distribution network for pressure optimization
    and accelerated leak detection.
    """

    HEURISTIC_ID = "H2"
    SPI_MIN = -1.8
    SPI_MAX = -1.2
    DAYS_MIN = 30
    DAYS_MAX = 45
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = ["H2_PRESSURE_REDUCTION", "H2_LEAK_DETECTION"]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for pressure management.

        Infrastructure measures typically higher priority for government.
        """
        # Base priority from SPI severity
        base = 55 + (abs(context.spi) - 1.2) * 25  # 55-70 range

        # Trend is already filtered to WORSENING, add bonus
        base += 10

        # Profile adjustment
        if context.profile == Profile.GOVERNMENT:
            base += 10  # Government prioritizes infrastructure
        else:
            base += 5

        # Days to critical - more urgent in the 30-35 day range
        if context.days_to_critical:
            if context.days_to_critical < 35:
                base += 10
            elif context.days_to_critical < 40:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for pressure management actions."""
        days_str = (
            f"{context.days_to_critical} days"
            if context.days_to_critical
            else "moderate time"
        )

        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), worsening trend. "
            f"Estimated {days_str} to critical threshold. "
            f"Network pressure management and leak detection recommended to reduce losses. "
            f"Expected impact: 10% pressure reduction = +4 days, leak repairs can add +2 days per 1% reduction."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters based on severity and profile."""
        # More aggressive pressure reduction for worse conditions
        if context.spi < -1.6:
            pressure_reduction = 15
            coverage = 90
        elif context.spi < -1.4:
            pressure_reduction = 12
            coverage = 80
        else:
            pressure_reduction = 10
            coverage = 75

        return {
            "pressure_reduction_pct": pressure_reduction,
            "hours_start": 23,
            "hours_end": 5,
            "leak_detection_coverage_pct": coverage,
            "repair_priority_threshold_lps": 1.0,
        }
