"""H15: Step-Down Recovery - Protocolo de Terminación Escalonada.

Requires positive SPI across ALL scales (3, 6, 12) for 2+ months before
allowing phased restriction relaxation, preventing premature termination.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H15StepdownRecovery(BaseHeuristic):
    """
    H15: Step-Down Recovery (Protocolo de Terminación Escalonada)

    Rationale:
    - Premature drought termination is a common management error
    - Lifting restrictions on SPI-3 improvement triggers demand rebound
    - Recovery must be validated across multiple time scales
    - Asymmetric entry/exit: easy to enter alerts, hard to exit
    - Phased relaxation: recreational → irrigation → industrial

    Activation:
    - SPI-3 > 0 AND SPI-6 > 0 AND SPI-12 > 0 AND
    - all_scales_positive_months >= 2

    Actions:
    - Phased restriction relaxation
    - Recovery monitoring protocol
    - Public announcement of recovery phase
    """

    HEURISTIC_ID = "H15"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H15_PHASED_RELAXATION",
        "H15_RECOVERY_MONITORING",
        "H15_PUBLIC_ANNOUNCEMENT",
    ]

    CONSECUTIVE_MONTHS_REQUIRED = 2

    def check_activation(self, context: HeuristicContext) -> bool:
        """All scales positive for sustained period."""
        all_positive = (
            context.spi_3 is not None and context.spi_3 > 0 and
            context.spi_6 is not None and context.spi_6 > 0 and
            context.spi_12 is not None and context.spi_12 > 0
        )

        sustained = (
            context.all_scales_positive_months >= self.CONSECUTIVE_MONTHS_REQUIRED
        )

        return all_positive and sustained

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Lower priority than emergency heuristics.
        Priority increases with sustained positive months.
        """
        base = 40

        # More months positive = more confidence in recovery
        if context.all_scales_positive_months >= 4:
            base += 15
        elif context.all_scales_positive_months >= 3:
            base += 10
        elif context.all_scales_positive_months >= 2:
            base += 5

        # Higher positive values = stronger recovery
        spi_min = min(
            context.spi_3 or 0,
            context.spi_6 or 0,
            context.spi_12 or 0
        )
        if spi_min > 0.5:
            base += 10
        elif spi_min > 0.2:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_3 = context.spi_3 if context.spi_3 is not None else 0
        spi_6 = context.spi_6 if context.spi_6 is not None else 0
        spi_12 = context.spi_12 if context.spi_12 is not None else 0
        months = context.all_scales_positive_months

        return (
            f"[RECUPERACIÓN CONFIRMADA] "
            f"SPI-3={spi_3:.2f}, SPI-6={spi_6:.2f}, SPI-12={spi_12:.2f}. "
            f"Todas las escalas positivas por {months} meses consecutivos. "
            f"Iniciar relajación escalonada: "
            f"1) Uso recreativo, 2) Riego limitado, 3) Industrial gradual. "
            f"Mantener monitoreo para prevenir recaída."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        months = context.all_scales_positive_months

        # Determine relaxation phase based on recovery duration
        if months >= 4:
            phase = 3
            relaxation_scope = ["recreational", "limited_irrigation", "industrial"]
        elif months >= 3:
            phase = 2
            relaxation_scope = ["recreational", "limited_irrigation"]
        else:
            phase = 1
            relaxation_scope = ["recreational"]

        return {
            "spi_3": context.spi_3,
            "spi_6": context.spi_6,
            "spi_12": context.spi_12,
            "all_scales_positive_months": months,
            "recovery_phase": phase,
            "relaxation_scope": relaxation_scope,
            "phase_duration_days": 30,
            "monitoring_frequency": "weekly",
            "reactivation_threshold_spi": -0.5,
        }
