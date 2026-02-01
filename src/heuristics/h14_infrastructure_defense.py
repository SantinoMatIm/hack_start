"""H14: Infrastructure Defense - Defensa de Infraestructura y Gestión de Presión.

Activates night pressure reduction and aggressive leak management when
extreme long-term drought coincides with system operating near capacity.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend, Profile


class H14InfrastructureDefense(BaseHeuristic):
    """
    H14: Infrastructure Defense (Defensa de Infraestructura y Gestión de Presión)

    Rationale:
    - Leak volume is proportional to system pressure
    - Night pressure reduction can cut "non-revenue water" by 15-20%
    - Cape Town's "Day Zero" crisis showed pressure management is critical
    - Only justified when both drought AND capacity constraints exist
    - Punitive tiered tariffs become necessary at this stage

    Activation:
    - SPI-24 < -2.0 AND
    - demand_capacity_ratio > 90%

    Actions:
    - Night pressure reduction (11pm-5am)
    - Accelerated leak detection/repair
    - Demand management tariffs
    """

    HEURISTIC_ID = "H14"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H14_NIGHT_PRESSURE_REDUCTION",
        "H14_DEMAND_MANAGEMENT",
        "H14_INFRASTRUCTURE_PROTECTION",
    ]

    SPI_24_THRESHOLD = -2.0
    DEMAND_CAPACITY_THRESHOLD = 0.90  # 90%

    def check_activation(self, context: HeuristicContext) -> bool:
        """Extreme long-term drought + system near capacity."""
        if context.spi_24 is None:
            return False

        spi_critical = context.spi_24 < self.SPI_24_THRESHOLD

        demand_critical = (
            context.demand_capacity_ratio is not None and
            context.demand_capacity_ratio > self.DEMAND_CAPACITY_THRESHOLD
        )

        return spi_critical and demand_critical

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - How close to capacity
        - SPI severity
        """
        base = 75

        # Closer to capacity = higher priority
        if context.demand_capacity_ratio is not None:
            if context.demand_capacity_ratio > 0.95:
                base += 15  # Almost at limit
            elif context.demand_capacity_ratio > 0.92:
                base += 10
            elif context.demand_capacity_ratio > 0.90:
                base += 5

        # More severe drought
        if context.spi_24 is not None:
            if context.spi_24 < -2.5:
                base += 10
            elif context.spi_24 < -2.2:
                base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_24 = context.spi_24 if context.spi_24 is not None else 0
        demand_ratio = context.demand_capacity_ratio or 0

        return (
            f"[DEFENSA DE INFRAESTRUCTURA] SPI-24 = {spi_24:.2f}, "
            f"Demanda/Capacidad = {demand_ratio*100:.0f}%. "
            f"Sistema operando cerca del límite crítico. "
            f"Reducción de presión nocturna (23:00-06:00) reduce pérdidas 15-20%. "
            f"Proteger infraestructura de estrés mecánico prolongado."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        demand_ratio = context.demand_capacity_ratio or 0

        # More stressed = more aggressive pressure reduction
        if demand_ratio > 0.95:
            pressure_reduction = 25
            hours_start = 22
            hours_end = 6
        elif demand_ratio > 0.92:
            pressure_reduction = 20
            hours_start = 23
            hours_end = 5
        else:
            pressure_reduction = 15
            hours_start = 23
            hours_end = 5

        return {
            "spi_24": context.spi_24,
            "demand_capacity_ratio": demand_ratio,
            "pressure_reduction_pct": pressure_reduction,
            "reduction_hours_start": hours_start,
            "reduction_hours_end": hours_end,
            "leak_repair_priority_threshold_lps": 0.5,
            "tiered_tariff_activation": True,
        }
