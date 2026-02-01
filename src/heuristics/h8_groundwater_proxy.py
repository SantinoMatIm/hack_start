"""H8: Groundwater Proxy - Gatillo de Recarga de Acuíferos.

Uses long-term SPI (24-48 months) as proxy for aquifer stress,
activating pumping restrictions to protect groundwater sustainability.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H8GroundwaterProxy(BaseHeuristic):
    """
    H8: Groundwater Proxy (Gatillo de Recarga de Acuíferos)

    Rationale:
    - Groundwater responds to very low-frequency climate patterns
    - SPI-24 and SPI-48 are excellent proxies for water table fluctuations
    - Multi-year deficits indicate recharge failure
    - Continued pumping during recharge failure risks aquifer collapse
    - Subsidence and water quality degradation are irreversible

    Activation:
    - SPI-24 < -1.5 OR SPI-48 < -1.5

    Actions:
    - Pumping restrictions for agricultural/industrial wells
    - Intensified aquifer monitoring
    - Alternative source activation
    """

    HEURISTIC_ID = "H8"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H8_PUMPING_RESTRICTION",
        "H8_AQUIFER_MONITORING",
        "H8_ALTERNATIVE_SOURCES",
    ]

    SPI_24_THRESHOLD = -1.5
    SPI_48_THRESHOLD = -1.5

    def check_activation(self, context: HeuristicContext) -> bool:
        """Long-term SPI indicates multi-year recharge deficit."""
        spi_24_critical = (
            context.spi_24 is not None and
            context.spi_24 < self.SPI_24_THRESHOLD
        )
        spi_48_critical = (
            context.spi_48 is not None and
            context.spi_48 < self.SPI_48_THRESHOLD
        )

        return spi_24_critical or spi_48_critical

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Severity of long-term deficit
        - Whether both scales are affected
        """
        base = 60

        # More severe long-term deficit = higher priority
        if context.spi_48 is not None:
            if context.spi_48 < -2.0:
                base += 20
            elif context.spi_48 < -1.7:
                base += 15
            elif context.spi_48 < -1.5:
                base += 10

        if context.spi_24 is not None:
            if context.spi_24 < -2.0:
                base += 15
            elif context.spi_24 < -1.7:
                base += 10

        # Both scales affected = compounded risk
        if (context.spi_24 is not None and context.spi_24 < self.SPI_24_THRESHOLD and
            context.spi_48 is not None and context.spi_48 < self.SPI_48_THRESHOLD):
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_24 = f"{context.spi_24:.2f}" if context.spi_24 is not None else "N/A"
        spi_48 = f"{context.spi_48:.2f}" if context.spi_48 is not None else "N/A"

        return (
            f"[ESTRÉS DE ACUÍFEROS] SPI-24={spi_24}, SPI-48={spi_48}. "
            f"Déficit de recarga multi-anual detectado. "
            f"Restricción de bombeo subterráneo recomendada para prevenir "
            f"agotamiento irreversible de acuíferos y subsidencia del terreno."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        # Determine severity tier
        spi_24 = context.spi_24 if context.spi_24 is not None else 0
        spi_48 = context.spi_48 if context.spi_48 is not None else 0
        worst_spi = min(spi_24, spi_48)

        if worst_spi < -2.0:
            reduction_pct = 30
            monitoring_frequency = "weekly"
        elif worst_spi < -1.7:
            reduction_pct = 25
            monitoring_frequency = "biweekly"
        else:
            reduction_pct = 20
            monitoring_frequency = "monthly"

        return {
            "spi_24": spi_24,
            "spi_48": spi_48,
            "pumping_reduction_pct": reduction_pct,
            "monitoring_frequency": monitoring_frequency,
            "affected_sectors": ["agricultural", "industrial"],
            "new_permits_suspended": True,
        }
