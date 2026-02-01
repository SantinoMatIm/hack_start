"""H13: Cooling Towers - Eficiencia Industrial Torres de Enfriamiento.

Mandates increased Cycles of Concentration (CoC) in industrial cooling
towers when SPI-12 indicates severe drought, achieving 20-40% water savings.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend, Profile


class H13CoolingTowers(BaseHeuristic):
    """
    H13: Cooling Towers (Eficiencia Industrial - Torres de Enfriamiento)

    Rationale:
    - Cooling towers are massive industrial water consumers
    - Cycles of Concentration (CoC) measures recirculation efficiency
    - Moving from CoC 2-3 to 5-6 can reduce makeup water by 20-40%
    - Higher CoC requires better chemical treatment (scaling/corrosion)
    - Severe drought justifies the operational cost increase

    Activation:
    - SPI-12 < -1.5

    Actions:
    - CoC mandate for large industrial users
    - Industrial water audit
    - Water treatment upgrade assistance
    """

    HEURISTIC_ID = "H13"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H13_COC_MANDATE",
        "H13_INDUSTRIAL_AUDIT",
        "H13_WATER_TREATMENT_UPGRADE",
    ]

    SPI_12_THRESHOLD = -1.5
    TARGET_COC_MIN = 5.0

    def check_activation(self, context: HeuristicContext) -> bool:
        """SPI-12 indicates severe drought requiring industrial efficiency."""
        if context.spi_12 is None:
            return False

        return context.spi_12 < self.SPI_12_THRESHOLD

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - SPI-12 severity
        - Profile (industry has higher priority)
        """
        base = 55

        # More severe = higher priority
        if context.spi_12 is not None:
            if context.spi_12 < -2.0:
                base += 20
            elif context.spi_12 < -1.7:
                base += 15
            elif context.spi_12 < -1.5:
                base += 10

        # Industry profile = more relevant
        if context.profile == Profile.INDUSTRY:
            base += 20
        else:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi_12 = context.spi_12 if context.spi_12 is not None else 0
        current_coc = context.industrial_coc_current or "desconocido"

        return (
            f"[TORRES DE ENFRIAMIENTO] SPI-12 = {spi_12:.2f}. "
            f"CoC actual: {current_coc}, objetivo: >= {self.TARGET_COC_MIN}. "
            f"Incrementar ciclos de concentración reduce consumo 20-40%. "
            f"Mandato aplicable a industrias con consumo > 5,000 m³/mes."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        spi_12 = context.spi_12 if context.spi_12 is not None else 0

        # More severe drought = stricter requirements
        if spi_12 < -2.0:
            target_coc = 6.0
            deadline_days = 30
        elif spi_12 < -1.7:
            target_coc = 5.5
            deadline_days = 45
        else:
            target_coc = 5.0
            deadline_days = 60

        return {
            "spi_12": spi_12,
            "current_coc": context.industrial_coc_current,
            "minimum_coc_required": target_coc,
            "compliance_deadline_days": deadline_days,
            "consumption_threshold_m3_month": 5000,
            "chemical_treatment_support": True,
            "estimated_water_savings_pct": "20-40",
        }
