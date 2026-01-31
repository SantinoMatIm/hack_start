"""H3: Public Communication Heuristic."""

from src.config.constants import Trend, Profile
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext


class H3PublicCommunication(BaseHeuristic):
    """
    H3: Public Communication Campaign

    Activation: SPI -2.0 to -1.0, Trend WORSENING, days > 30
    Impact: 3% reduction = +2 days

    Public awareness campaigns and education programs to
    encourage voluntary conservation.
    """

    HEURISTIC_ID = "H3"
    SPI_MIN = -2.0
    SPI_MAX = -1.0
    DAYS_MIN = 30
    DAYS_MAX = None
    ALLOWED_TRENDS = (Trend.WORSENING,)
    APPLICABLE_ACTION_CODES = ["H3_AWARENESS_CAMPAIGN", "H3_SCHOOL_PROGRAM", "H3_HOTLINE_LAUNCH"]

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority for communication actions.

        Government profile prioritizes public-facing measures.
        """
        # Base priority - communication is generally medium priority
        base = 45 + (abs(context.spi) - 1.0) * 15  # 45-60 range

        # Trend adjustment
        if context.trend == Trend.WORSENING:
            base += 5

        # Profile adjustment
        if context.profile == Profile.GOVERNMENT:
            base += 15  # Government prioritizes public communication
        else:
            base += 5

        # Days to critical adjustment
        if context.days_to_critical:
            if context.days_to_critical < 45:
                base += 5
            if context.days_to_critical < 35:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        """Generate justification for public communication actions."""
        severity = "severe" if context.spi < -1.5 else "elevated"

        return (
            f"SPI-6 = {context.spi:.2f} ({context.risk_level.value}), worsening trend indicates {severity} drought risk. "
            f"Public communication campaigns recommended to drive voluntary conservation. "
            f"Historical data shows 3-5% consumption reduction achievable through awareness, providing +2-3 days buffer."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """Get default parameters based on severity."""
        # Determine campaign intensity
        if context.spi < -1.5:
            intensity = "emergency"
            channels = ["tv", "radio", "social_media", "billboards"]
            schools_pct = 80
        elif context.spi < -1.3:
            intensity = "high"
            channels = ["tv", "radio", "social_media"]
            schools_pct = 60
        else:
            intensity = "moderate"
            channels = ["social_media", "radio"]
            schools_pct = 50

        return {
            "campaign_intensity": intensity,
            "channels": channels,
            "schools_pct": schools_pct,
            "grade_levels": "both",
            "launch_hotline": context.spi < -1.3,
        }
