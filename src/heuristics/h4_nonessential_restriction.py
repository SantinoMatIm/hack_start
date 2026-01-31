"""H4: Non-Essential Water Use Restriction Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H4NonessentialRestriction(BaseHeuristic):
    """
    H4: Non-Essential Water Use Restriction

    Activation: SPI <= -1.8, Trend WORSENING, days < 30
    Impact: 1% removed = +1.3 days

    Mandatory restrictions on non-essential water uses like
    lawn irrigation, car washing, pool filling, and fountains.
    """

    HEURISTIC_ID = "H4"
    SPI_MIN = float("-inf")
    SPI_MAX = -1.8
    DAYS_MIN = None
    DAYS_MAX = 30
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = [
        "H4_LAWN_BAN",
        "H4_CARWASH_RESTRICTION",
        "H4_POOL_RESTRICTION",
        "H4_FOUNTAIN_SHUTDOWN",
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for restriction actions.

        High priority due to urgency (< 30 days to critical).
        """
        # Base priority - restrictions are high priority when triggered
        base = 70 + (abs(context.spi) - 1.8) * 20  # 70-90 range

        # Trend adjustment (already filtered to WORSENING)
        base += 5

        # Profile adjustment
        if context.profile == Profile.GOVERNMENT:
            base += 5  # Government can enforce restrictions
        else:
            base += 10  # Industry needs to prepare for restrictions

        # Days to critical - very urgent for this heuristic
        if context.days_to_critical:
            if context.days_to_critical < 15:
                base += 15
            elif context.days_to_critical < 20:
                base += 10
            elif context.days_to_critical < 25:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for restriction actions."""
        days_str = (
            f"{context.days_to_critical} days"
            if context.days_to_critical
            else "limited time"
        )
        urgency = "URGENT" if context.days_to_critical and context.days_to_critical < 20 else "HIGH PRIORITY"

        return (
            f"[{urgency}] SPI-6 = {context.spi:.2f} ({context.risk_level.value}), worsening trend with only {days_str} to critical. "
            f"Non-essential water use restrictions are necessary to extend supply. "
            f"Lawn irrigation, car washing, and decorative fountains account for 5-8% of urban consumption. "
            f"Restrictions can add +6-10 days to water supply timeline."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters based on urgency."""
        # More restrictive for more urgent situations
        if context.days_to_critical and context.days_to_critical < 15:
            # Severe restrictions
            return {
                "lawn_hours_per_day": 0,
                "lawn_days_per_week": 0,
                "lawn_compliance_target": 95,
                "carwash_commercial_days": 2,
                "carwash_home_ban": True,
                "pool_types_affected": "all",
                "fountain_scope": "all",
            }
        elif context.days_to_critical and context.days_to_critical < 25:
            # Moderate restrictions
            return {
                "lawn_hours_per_day": 1,
                "lawn_days_per_week": 2,
                "lawn_compliance_target": 85,
                "carwash_commercial_days": 3,
                "carwash_home_ban": True,
                "pool_types_affected": "private",
                "fountain_scope": "all",
            }
        else:
            # Baseline restrictions
            return {
                "lawn_hours_per_day": 2,
                "lawn_days_per_week": 2,
                "lawn_compliance_target": 80,
                "carwash_commercial_days": 4,
                "carwash_home_ban": True,
                "pool_types_affected": "private",
                "fountain_scope": "commercial_only",
            }
