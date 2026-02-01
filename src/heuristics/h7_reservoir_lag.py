"""H7: Reservoir Lag - Inercia Hidrológica.

Prevents premature relaxation of restrictions by requiring both SPI recovery
AND physical reservoir storage verification before allowing step-down.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend, Profile


class H7ReservoirLag(BaseHeuristic):
    """
    H7: Reservoir Lag (Inercia Hidrológica)

    Rationale:
    - Surface water storage and river baseflows are low-pass filters of climate
    - Significant lag between rainfall start and reservoir recovery
    - Soil must saturate before generating runoff
    - Lifting restrictions on short-term SPI improvement causes recurring crises

    Activation:
    - (SPI-6 > SPI-12 AND SPI-12 < -1.0), OR
    - reservoir_storage_pct < 60%

    Actions:
    - Hold current restrictions
    - Require reservoir level validation
    - Phased relaxation protocol
    """

    HEURISTIC_ID = "H7"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H7_RESTRICTION_HOLD",
        "H7_RESERVOIR_VALIDATION",
        "H7_PHASED_RELAXATION",
    ]

    SPI_12_THRESHOLD = -1.0
    RESERVOIR_MIN_PCT = 60

    def check_activation(self, context: HeuristicContext) -> bool:
        """
        Activate when:
        1. Short-term improving but long-term still deficit, OR
        2. Reservoir storage below safe threshold
        """
        if context.spi_12 is None:
            return False

        # Short-term better than long-term = false recovery risk
        short_term_improving = (
            context.spi_6 is not None and
            context.spi_6 > context.spi_12
        )
        long_term_deficit = context.spi_12 < self.SPI_12_THRESHOLD

        scale_divergence = short_term_improving and long_term_deficit

        # Low reservoir regardless of SPI
        reservoir_low = (
            context.reservoir_storage_pct is not None and
            context.reservoir_storage_pct < self.RESERVOIR_MIN_PCT
        )

        return scale_divergence or reservoir_low

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - How low reservoir storage is
        - Magnitude of SPI divergence
        """
        base = 55

        # Lower reservoir = higher priority
        if context.reservoir_storage_pct is not None:
            if context.reservoir_storage_pct < 40:
                base += 25
            elif context.reservoir_storage_pct < 50:
                base += 15
            elif context.reservoir_storage_pct < 60:
                base += 10

        # Larger scale divergence = higher risk of false recovery
        if context.spi_6 is not None and context.spi_12 is not None:
            divergence = context.spi_6 - context.spi_12
            base += min(15, divergence * 10)

        # Government profile has more responsibility for public supply
        if context.profile == Profile.GOVERNMENT:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_6 = context.spi_6 if context.spi_6 is not None else "N/A"
        spi_12 = context.spi_12 if context.spi_12 is not None else "N/A"
        reservoir = context.reservoir_storage_pct

        reservoir_str = f"{reservoir:.0f}%" if reservoir is not None else "sin datos"

        return (
            f"[INERCIA HIDROLÓGICA] SPI-6={spi_6} vs SPI-12={spi_12}. "
            f"Almacenamiento en embalses: {reservoir_str}. "
            f"Mejora reciente en precipitación NO significa recuperación hidrológica. "
            f"MANTENER restricciones hasta SPI-12 > -1.0 Y embalses > 60%."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        reservoir = context.reservoir_storage_pct or 0

        return {
            "spi_6": context.spi_6,
            "spi_12": context.spi_12,
            "reservoir_storage_pct": reservoir,
            "restriction_hold": True,
            "reservoir_threshold_for_relaxation": 60,
            "spi_12_threshold_for_relaxation": -1.0,
            "relaxation_blocked_reason": (
                "reservoir_low" if reservoir < 60 else "spi_12_deficit"
            ),
        }
