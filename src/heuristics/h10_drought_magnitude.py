"""H10: Drought Magnitude - Magnitud Acumulada del Evento.

Uses run theory to calculate cumulative drought severity, triggering
scaled responses based on historical percentile ranking.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H10DroughtMagnitude(BaseHeuristic):
    """
    H10: Drought Magnitude (Magnitud Acumulada del Evento)

    Rationale:
    - Impact = f(intensity × duration), not just peak SPI
    - A 5-year mild drought often worse than 3-month extreme drought
    - Cumulative magnitude captures economic/ecological exhaustion
    - Historical percentile provides context for response scaling

    Activation:
    - magnitude_percentile >= 50 (current event in top 50% historically)

    Actions:
    - Magnitude-based response scaling
    - Historical comparison reporting
    - Escalated emergency measures
    """

    HEURISTIC_ID = "H10"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H10_MAGNITUDE_BASED_RESPONSE",
        "H10_HISTORICAL_COMPARISON",
        "H10_ESCALATED_MEASURES",
    ]

    PERCENTILE_THRESHOLD_MODERATE = 50
    PERCENTILE_THRESHOLD_SEVERE = 75
    PERCENTILE_THRESHOLD_EXTREME = 90

    def check_activation(self, context: HeuristicContext) -> bool:
        """Activate when current drought magnitude exceeds historical median."""
        if context.magnitude_percentile is None:
            return False

        return context.magnitude_percentile >= self.PERCENTILE_THRESHOLD_MODERATE

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on percentile tier:
        - Top 50%: moderate
        - Top 25%: high
        - Top 10%: critical
        """
        if context.magnitude_percentile is None:
            return 0

        percentile = context.magnitude_percentile

        if percentile >= self.PERCENTILE_THRESHOLD_EXTREME:
            return 90
        elif percentile >= self.PERCENTILE_THRESHOLD_SEVERE:
            return 75
        elif percentile >= self.PERCENTILE_THRESHOLD_MODERATE:
            return 55
        else:
            return 0

    def generate_justification(self, context: HeuristicContext) -> str:
        magnitude = context.drought_magnitude or 0
        percentile = context.magnitude_percentile or 0
        duration = context.drought_duration_months
        tier = context.severity_tier or self._get_tier(percentile)

        return (
            f"[MAGNITUD ACUMULADA - {tier.upper()}] "
            f"Magnitud = {magnitude:.2f}, Duración = {duration} meses, "
            f"Percentil histórico = {percentile:.0f}%. "
            f"Esta sequía ya supera el {percentile:.0f}% de eventos históricos. "
            f"Escalar intensidad de respuesta acorde a severidad acumulada."
        )

    def _get_tier(self, percentile: float) -> str:
        if percentile >= self.PERCENTILE_THRESHOLD_EXTREME:
            return "extreme"
        elif percentile >= self.PERCENTILE_THRESHOLD_SEVERE:
            return "severe"
        elif percentile >= self.PERCENTILE_THRESHOLD_MODERATE:
            return "moderate"
        else:
            return "below_average"

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        percentile = context.magnitude_percentile or 0
        tier = self._get_tier(percentile)

        response_levels = {
            "extreme": {
                "response_tier": "tier_3",
                "resource_multiplier": 2.0,
                "coordination_level": "national",
            },
            "severe": {
                "response_tier": "tier_2",
                "resource_multiplier": 1.5,
                "coordination_level": "state",
            },
            "moderate": {
                "response_tier": "tier_1",
                "resource_multiplier": 1.2,
                "coordination_level": "municipal",
            },
            "below_average": {
                "response_tier": "baseline",
                "resource_multiplier": 1.0,
                "coordination_level": "local",
            },
        }

        params = response_levels.get(tier, response_levels["moderate"])
        params.update({
            "drought_magnitude": context.drought_magnitude,
            "magnitude_percentile": percentile,
            "drought_duration_months": context.drought_duration_months,
            "severity_tier": tier,
        })

        return params
