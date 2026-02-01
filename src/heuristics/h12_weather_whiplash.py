"""H12: Weather Whiplash - Gestión de Volatilidad.

Detects rapid transitions from wet to dry conditions within 12 months,
triggering maximum conservation due to infrastructure stress and
reduced infiltration capacity.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H12WeatherWhiplash(BaseHeuristic):
    """
    H12: Weather Whiplash (Gestión de Volatilidad)

    Rationale:
    - Climate change increases frequency of wet-dry extremes
    - Rapid transitions stress infrastructure (pipes, reservoirs)
    - Soil compaction during dry phase reduces infiltration
    - Traditional reservoir operation (empty for flood control) fails
    - Requires more conservative water retention strategy

    Activation:
    - recent_wet_to_dry_transition = True AND
    - months_since_wet_period < 12

    Actions:
    - Maximum conservation mandate
    - Infrastructure stress assessment
    - Volatility-aware reservoir management
    """

    HEURISTIC_ID = "H12"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H12_MAXIMUM_CONSERVATION",
        "H12_INFRASTRUCTURE_PROTECTION",
        "H12_VOLATILITY_MANAGEMENT",
    ]

    TRANSITION_MONTHS_THRESHOLD = 12

    def check_activation(self, context: HeuristicContext) -> bool:
        """Detect rapid wet-to-dry transition."""
        if not context.recent_wet_to_dry_transition:
            return False

        if context.months_since_wet_period is None:
            return False

        return context.months_since_wet_period < self.TRANSITION_MONTHS_THRESHOLD

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Speed of transition (fewer months = higher priority)
        - Severity of current dry conditions
        """
        base = 65

        # Faster transition = higher stress
        if context.months_since_wet_period is not None:
            if context.months_since_wet_period < 6:
                base += 20
            elif context.months_since_wet_period < 9:
                base += 10
            else:
                base += 5

        # Current drought severity
        spi = context.spi_6 if context.spi_6 is not None else 0
        if spi < -1.5:
            base += 10
        elif spi < -1.0:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        months = context.months_since_wet_period or 0
        spi = context.spi_6 if context.spi_6 is not None else 0

        return (
            f"[WEATHER WHIPLASH] Transición húmedo→seco en {months} meses. "
            f"SPI-6 actual: {spi:.2f}. "
            f"Infraestructura hídrica estresada por cambio climático rápido. "
            f"Suelos compactados reducen infiltración. "
            f"Conservación máxima requerida hasta estabilización."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        months = context.months_since_wet_period or 0

        # Faster transition = more aggressive conservation
        if months < 6:
            conservation_target = 20
            infrastructure_priority = "critical"
        elif months < 9:
            conservation_target = 15
            infrastructure_priority = "high"
        else:
            conservation_target = 12
            infrastructure_priority = "elevated"

        return {
            "months_since_wet_period": months,
            "conservation_target_pct": conservation_target,
            "infrastructure_assessment_priority": infrastructure_priority,
            "reservoir_management_mode": "conservative_retention",
            "soil_infiltration_monitoring": True,
        }
