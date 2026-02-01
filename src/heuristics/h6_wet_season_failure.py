"""H6: Wet Season Failure - Anomalía Estacional Compuesta.

Implements a "latch" mechanism when the wet season fails, preventing
premature relaxation of restrictions until the next successful wet season.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H6WetSeasonFailure(BaseHeuristic):
    """
    H6: Wet Season Failure (Anomalía Estacional Compuesta)

    Rationale:
    - In seasonal climates, hydrological recharge occurs only in wet season
    - If wet season fails, recovery is physically impossible until next cycle
    - Sporadic dry-season rains may improve short-term SPI but not reservoirs
    - "Latch" mechanism prevents false recovery signals

    Activation:
    - wet_season_locked = True (previous failure still active), OR
    - wet_season_average_spi < -1.0 (new failure detected)

    Actions:
    - Sustained restrictions throughout dry season
    - Long-term planning engagement
    - Reserve management protocols
    """

    HEURISTIC_ID = "H6"
    REQUIRES_SEASONALITY = True

    APPLICABLE_ACTION_CODES = [
        "H6_SUSTAINED_RESTRICTIONS",
        "H6_LONG_TERM_PLANNING",
        "H6_RESERVE_MANAGEMENT",
    ]

    WET_SEASON_SPI_THRESHOLD = -1.0

    def check_activation(self, context: HeuristicContext) -> bool:
        """Activate if wet season failed or latch is still engaged."""
        # Latch mechanism: once locked, stay locked
        if context.wet_season_locked:
            return True

        # New failure detection
        if context.wet_season_average_spi is None:
            return False

        return context.wet_season_average_spi < self.WET_SEASON_SPI_THRESHOLD

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Severity of wet season failure
        - Whether latch is already engaged
        """
        base = 65

        # Already locked = confirmed structural deficit
        if context.wet_season_locked:
            base += 15

        # Severity of failure
        if context.wet_season_average_spi is not None:
            if context.wet_season_average_spi < -1.5:
                base += 10
            elif context.wet_season_average_spi < -1.2:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        avg_spi = context.wet_season_average_spi
        avg_str = f"{avg_spi:.2f}" if avg_spi is not None else "N/A"

        if context.wet_season_locked:
            return (
                f"[CERROJO ESTACIONAL ACTIVO] "
                f"SPI promedio temporada húmeda = {avg_str}. "
                f"Recarga hídrica insuficiente en ciclo anterior. "
                f"CERROJO ACTIVO: mantener restricciones hasta próxima temporada húmeda exitosa. "
                f"No relajar medidas aunque SPI de corto plazo mejore."
            )
        else:
            return (
                f"[FALLA DE TEMPORADA HÚMEDA] "
                f"SPI promedio temporada húmeda = {avg_str}. "
                f"Recarga hídrica insuficiente detectada. "
                f"Activando cerrojo de restricciones hasta próximo ciclo. "
                f"Déficit estructural no recuperable en temporada seca."
            )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        return {
            "wet_season_locked": context.wet_season_locked,
            "wet_season_average_spi": context.wet_season_average_spi,
            "restriction_duration": "until_next_wet_season",
            "review_period_days": 90,
            "minimum_wet_season_spi_to_unlock": 0.0,
        }
