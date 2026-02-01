"""H1: Persistence Trigger - Gatillo de Inicio Confirmado.

Activates when SPI-3 falls below -1.0 for two consecutive periods,
confirming the establishment of a drought pattern rather than
transient meteorological noise.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H1PersistenceTrigger(BaseHeuristic):
    """
    H1: Persistence Trigger (Gatillo de Inicio Confirmado)

    Rationale:
    - SPI-1 is too volatile for reliable drought detection
    - SPI-3 correlates better with soil moisture availability
    - Requiring 2 consecutive dry periods filters stochastic noise
    - Acts as a low-pass filter for drought signal confirmation

    Activation:
    - SPI-3 < -1.0 for 2+ consecutive periods

    Actions:
    - Intensify monitoring frequency
    - Alert stakeholders
    - Pre-position response resources
    """

    HEURISTIC_ID = "H1"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H1_MONITORING_INTENSIFICATION",
        "H1_STAKEHOLDER_ALERT",
        "H1_RESOURCE_PREPOSITION",
    ]

    SPI_3_THRESHOLD = -1.0
    CONSECUTIVE_PERIODS_REQUIRED = 2

    def check_activation(self, context: HeuristicContext) -> bool:
        """SPI-3 < -1.0 for 2+ consecutive periods."""
        if context.spi_3 is None:
            return False

        return (
            context.spi_3 < self.SPI_3_THRESHOLD and
            context.consecutive_dry_periods >= self.CONSECUTIVE_PERIODS_REQUIRED
        )

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority increases with:
        - More consecutive dry periods
        - Lower SPI-3 values
        """
        base = 50

        # More consecutive periods = higher urgency
        base += min(20, (context.consecutive_dry_periods - 2) * 5)

        # Lower SPI = higher priority
        if context.spi_3 is not None:
            if context.spi_3 < -1.5:
                base += 15
            elif context.spi_3 < -1.3:
                base += 10

        # Worsening trend increases priority
        if context.trend == Trend.WORSENING:
            base += 10

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_3 = context.spi_3 if context.spi_3 is not None else 0
        return (
            f"[INICIO CONFIRMADO] SPI-3 = {spi_3:.2f} por "
            f"{context.consecutive_dry_periods} periodos consecutivos. "
            f"Patrón de sequía meteorológica establecido. "
            f"Se requiere intensificar monitoreo y preposicionar recursos de respuesta."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        return {
            "monitoring_frequency": "weekly",
            "alert_sectors": ["agricultural", "municipal", "industrial"],
            "resource_preposition_level": (
                "high" if context.consecutive_dry_periods >= 4 else "moderate"
            ),
        }
