"""H4: Phenological Stress - Umbral de Estrés Fenológico.

Elevates drought severity during critical crop growth stages
(flowering, grain filling) where water stress causes disproportionate
yield losses.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend, Profile


class H4PhenologicalStress(BaseHeuristic):
    """
    H4: Phenological Stress (Umbral de Estrés Fenológico)

    Rationale:
    - Drought impact on crops is highly non-linear with respect to timing
    - Moderate drought during flowering can cause 100% yield loss
    - Same drought during vegetative stage may have minimal impact
    - SPI-12 masks these critical-window deficits

    Activation:
    - (SPI-3 < -1.5 OR SPI-6 < -1.5) AND
    - Currently in critical phenological window (flowering, grain filling)

    Actions:
    - Agricultural alert to producers
    - Prioritize irrigation allocation
    - Activate crop insurance triggers
    """

    HEURISTIC_ID = "H4"
    REQUIRES_PHENOLOGY = True
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H4_AGRICULTURAL_ALERT",
        "H4_IRRIGATION_PRIORITY",
        "H4_CROP_INSURANCE_ACTIVATION",
    ]

    SPI_THRESHOLD = -1.5
    MOST_CRITICAL_STAGES = ["floracion", "llenado", "llenado_grano", "espigado"]

    def check_activation(self, context: HeuristicContext) -> bool:
        """SPI-3 or SPI-6 below threshold during critical phenological window."""
        if not context.is_critical_phenological_window:
            return False

        spi_3_critical = (
            context.spi_3 is not None and
            context.spi_3 < self.SPI_THRESHOLD
        )
        spi_6_critical = (
            context.spi_6 is not None and
            context.spi_6 < self.SPI_THRESHOLD
        )

        return spi_3_critical or spi_6_critical

    def _is_most_critical_stage(self, context: HeuristicContext) -> bool:
        """Check if currently in most critical stages (flowering, grain fill)."""
        for stage in context.phenological_stages:
            for critical in self.MOST_CRITICAL_STAGES:
                if critical in stage.lower():
                    return True
        return False

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Phenological stage criticality
        - SPI severity
        - Number of crops affected
        """
        base = 70  # High base priority for agricultural impact

        # Most critical stages (flowering, grain fill) get highest priority
        if self._is_most_critical_stage(context):
            base += 15
        else:
            base += 8

        # More crops affected = higher priority
        base += min(10, len(context.crops_affected) * 3)

        # Lower SPI = higher priority
        spi = context.spi_3 if context.spi_3 is not None else (context.spi_6 or 0)
        if spi < -2.0:
            base += 10
        elif spi < -1.7:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_3 = context.spi_3 if context.spi_3 is not None else "N/A"
        spi_6 = context.spi_6 if context.spi_6 is not None else "N/A"
        crops = ", ".join(context.crops_affected) if context.crops_affected else "cultivos"
        stages = ", ".join(context.phenological_stages) if context.phenological_stages else "etapa crítica"

        is_most_critical = self._is_most_critical_stage(context)
        severity = "MUY ALTO" if is_most_critical else "ALTO"

        return (
            f"[ESTRÉS FENOLÓGICO - {severity}] "
            f"SPI-3={spi_3}, SPI-6={spi_6}. "
            f"Ventana crítica activa para: {crops}. "
            f"Etapas: {stages}. "
            f"Impacto potencial severo en rendimientos agrícolas. "
            f"Priorizar asignación de agua para riego de rescate."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        is_most_critical = self._is_most_critical_stage(context)

        return {
            "crops_affected": context.crops_affected,
            "phenological_stages": context.phenological_stages,
            "alert_urgency": "critical" if is_most_critical else "high",
            "irrigation_allocation_pct": 35 if is_most_critical else 25,
            "insurance_trigger_enabled": True,
            "severity_multiplier": context.phenological_severity_multiplier,
        }
