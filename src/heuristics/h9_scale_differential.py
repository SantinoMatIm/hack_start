"""H9: Scale Differential - Diferencial de Escalas (Green Drought Paradox).

Detects false recovery signals when short-term SPI improves but
long-term deficit persists, preventing premature public relaxation.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H9ScaleDifferential(BaseHeuristic):
    """
    H9: Scale Differential (Diferencial de Escalas - Green Drought Paradox)

    Rationale:
    - Recent rain "greens" the landscape, reducing public conservation will
    - Visual recovery does not mean hydrological recovery
    - Large divergence between SPI-1 and SPI-12 indicates "Green Drought"
    - Critical for public communication to maintain conservation behavior

    Activation:
    - |SPI-1 - SPI-12| > 1.5 AND
    - SPI-12 < -1.0 AND
    - SPI-1 > SPI-12 (short-term appears better)

    Actions:
    - False recovery alert
    - Sustained public monitoring
    - Strategic communication campaign
    """

    HEURISTIC_ID = "H9"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H9_FALSE_RECOVERY_ALERT",
        "H9_SUSTAINED_MONITORING",
        "H9_PUBLIC_COMMUNICATION",
    ]

    DIFFERENTIAL_THRESHOLD = 1.5
    SPI_12_THRESHOLD = -1.0

    def check_activation(self, context: HeuristicContext) -> bool:
        """Detect significant divergence between short and long-term SPI."""
        if context.spi_1 is None or context.spi_12 is None:
            return False

        differential = abs(context.spi_1 - context.spi_12)

        return (
            differential > self.DIFFERENTIAL_THRESHOLD and
            context.spi_12 < self.SPI_12_THRESHOLD and
            context.spi_1 > context.spi_12  # Short-term appears better
        )

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Size of the differential
        - Severity of underlying long-term drought
        """
        base = 55

        # Larger differential = more deceptive conditions
        if context.scale_differential is not None:
            base += min(15, (context.scale_differential - 1.5) * 10)
        elif context.spi_1 is not None and context.spi_12 is not None:
            diff = abs(context.spi_1 - context.spi_12)
            base += min(15, (diff - 1.5) * 10)

        # More severe underlying drought = higher priority
        if context.spi_12 is not None:
            if context.spi_12 < -1.5:
                base += 15
            elif context.spi_12 < -1.2:
                base += 10

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_1 = context.spi_1 if context.spi_1 is not None else 0
        spi_12 = context.spi_12 if context.spi_12 is not None else 0
        differential = abs(spi_1 - spi_12)

        return (
            f"[FALSA RECUPERACIÓN - SEQUÍA VERDE] "
            f"SPI-1={spi_1:.2f} vs SPI-12={spi_12:.2f}. "
            f"Diferencial: {differential:.2f} unidades. "
            f"Lluvia reciente NO indica fin de sequía. "
            f"Déficit estructural persiste. "
            f"Comunicar activamente al público para mantener comportamiento de conservación."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        spi_1 = context.spi_1 if context.spi_1 is not None else 0
        spi_12 = context.spi_12 if context.spi_12 is not None else 0

        return {
            "spi_1": spi_1,
            "spi_12": spi_12,
            "scale_differential": abs(spi_1 - spi_12),
            "false_recovery_detected": True,
            "communication_channels": ["media", "social_media", "official"],
            "key_message": (
                "El paisaje se ve verde, pero los embalses siguen en crisis. "
                "Continúe conservando agua."
            ),
        }
