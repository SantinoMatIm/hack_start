"""H2: Flash Drought Detection - Índice de Intensificación Rápida.

Detects rapid drought intensification (flash drought) characterized by
a drop of 2+ SPI categories within 4 weeks, which can devastate crops
before traditional monthly monitoring can react.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H2FlashDrought(BaseHeuristic):
    """
    H2: Flash Drought Detection (Índice de Intensificación Rápida)

    Rationale:
    - Flash drought is driven by evapotranspiration anomalies, not just lack of rain
    - Traditional SPI threshold methods are too slow to detect it
    - Rate of intensification is more important than absolute magnitude initially
    - Can devastate crops in weeks during critical growth stages

    Activation:
    - SPI category drop >= 2 within 4 weeks
    - Categories: 0=Wet, 1=Normal, 2=Mild, 3=Moderate, 4=Severe, 5=Extreme

    Actions:
    - Flash drought alert
    - Rapid response activation
    - Emergency communication to agricultural sector
    """

    HEURISTIC_ID = "H2"
    REQUIRES_MULTI_SCALE_SPI = True

    APPLICABLE_ACTION_CODES = [
        "H2_FLASH_DROUGHT_ALERT",
        "H2_RAPID_RESPONSE_ACTIVATION",
        "H2_EMERGENCY_COMMUNICATION",
    ]

    CATEGORY_DROP_THRESHOLD = 2

    def check_activation(self, context: HeuristicContext) -> bool:
        """Detect 2+ category SPI drop within 4 weeks."""
        if context.current_spi_category is None:
            return False
        if context.spi_category_4_weeks_ago is None:
            return False

        # Higher category = drier conditions
        category_drop = (
            context.current_spi_category - context.spi_category_4_weeks_ago
        )

        return category_drop >= self.CATEGORY_DROP_THRESHOLD

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority increases with:
        - Larger category drops
        - Already dry conditions
        - Critical phenological windows
        """
        base = 75  # High base priority due to rapid nature

        # Larger drops = higher priority
        if context.current_spi_category is not None and context.spi_category_4_weeks_ago is not None:
            category_drop = context.current_spi_category - context.spi_category_4_weeks_ago
            base += min(20, (category_drop - 2) * 8)

        # Already in severe conditions
        if context.current_spi_category is not None and context.current_spi_category >= 4:
            base += 5

        # Phenological stress compounds the urgency
        if context.is_critical_phenological_window:
            base += 10

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        cat_prev = context.spi_category_4_weeks_ago or 0
        cat_curr = context.current_spi_category or 0
        drop = cat_curr - cat_prev

        category_names = ["Húmedo", "Normal", "Leve", "Moderado", "Severo", "Extremo"]
        prev_name = category_names[min(cat_prev, 5)]
        curr_name = category_names[min(cat_curr, 5)]

        return (
            f"[SEQUÍA RELÁMPAGO] Deterioro rápido detectado: "
            f"caída de {drop} categorías SPI en 4 semanas "
            f"({prev_name} → {curr_name}). "
            f"Velocidad de intensificación anormal. "
            f"Se requiere respuesta acelerada para proteger cultivos."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        cat_curr = context.current_spi_category or 0

        if cat_curr >= 4:
            alert_level = "critical"
            response_teams = 8
        elif cat_curr >= 3:
            alert_level = "urgent"
            response_teams = 5
        else:
            alert_level = "warning"
            response_teams = 3

        return {
            "alert_level": alert_level,
            "response_teams": response_teams,
            "priority_sectors": ["agricultural", "livestock"],
            "communication_channels": ["sms", "radio", "social_media"],
        }
