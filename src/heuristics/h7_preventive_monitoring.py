"""H7: Preventive Monitoring Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H7PreventiveMonitoring(BaseHeuristic):
    """
    H7: Preventive Monitoring and Early Action

    Activation: SPI -1.5 to -1.0, Trend STABLE, days 30-50
    Impact: Proactive measures before conditions worsen

    Covers the gap between H1 (days > 45) and H2 (requires WORSENING).
    Targets early intervention when conditions are stable but concerning.
    """

    HEURISTIC_ID = "H7"
    SPI_MIN = -1.5
    SPI_MAX = -1.0
    DAYS_MIN = 30
    DAYS_MAX = 50
    ALLOWED_TRENDS = (Trend.STABLE,)
    APPLICABLE_ACTION_CODES = [
        "H3_AWARENESS_CAMPAIGN",  # Public awareness
        "H2_LEAK_DETECTION",       # Infrastructure check
        "H1_INDUSTRIAL_AUDIT",     # Industrial efficiency
    ]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for preventive monitoring.

        Lower priority than urgent heuristics but important for early action.
        """
        # Base priority - moderate since conditions are stable
        base = 40 + (abs(context.spi) - 1.0) * 20  # 40-50 range

        # Days to critical adjustment
        if context.days_to_critical:
            if context.days_to_critical < 40:
                base += 10
            elif context.days_to_critical < 45:
                base += 5

        # Profile adjustment
        if context.profile == Profile.GOVERNMENT:
            base += 10  # Government prefers proactive measures
        else:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for preventive monitoring actions."""
        days_str = (
            f"{context.days_to_critical} days"
            if context.days_to_critical
            else "moderate time"
        )

        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), stable trend with {days_str} to critical. "
            f"Conditions are concerning but not yet worsening. "
            f"Preventive measures recommended: public awareness, leak detection, and industrial audits. "
            f"Early action can prevent escalation and provide buffer time."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters for preventive actions."""
        # Moderate intensity since conditions are stable
        return {
            "awareness_intensity": "moderate",
            "awareness_channels": ["social_media", "radio"],
            "leak_detection_coverage_pct": 60,
            "industrial_audit_threshold_m3": 12000,
            "monitoring_frequency": "weekly",
        }
