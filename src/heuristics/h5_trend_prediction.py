"""H5: Trend Prediction - Pendiente de Degradación Sostenida.

Uses Mann-Kendall test and Sen slope to detect statistically significant
degradation trends, allowing proactive measures before thresholds are crossed.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H5TrendPrediction(BaseHeuristic):
    """
    H5: Trend Prediction (Pendiente de Degradación Sostenida)

    Rationale:
    - Most alert systems are reactive: wait for threshold crossing
    - Drought has inertia: negative feedback loops reinforce drying
    - Detecting direction of change allows anticipating worsening
    - Statistical confidence prevents false trend signals

    Activation:
    - Sen slope < -0.1 SPI units/month AND
    - Mann-Kendall confidence >= 90%
    - Trend direction = "decreasing"

    Actions:
    - Trend alert to planners
    - Scenario projection
    - Preemptive restrictions
    """

    HEURISTIC_ID = "H5"
    REQUIRES_STATISTICAL_ANALYSIS = True

    APPLICABLE_ACTION_CODES = [
        "H5_TREND_ALERT",
        "H5_SCENARIO_PROJECTION",
        "H5_PREEMPTIVE_RESTRICTIONS",
    ]

    SEN_SLOPE_THRESHOLD = -0.1  # SPI units per month
    MANN_KENDALL_CONFIDENCE_THRESHOLD = 90.0  # percent

    def check_activation(self, context: HeuristicContext) -> bool:
        """Statistically significant negative trend detected."""
        if context.sen_slope_per_month is None:
            return False
        if context.mann_kendall_confidence is None:
            return False

        return (
            context.sen_slope_per_month < self.SEN_SLOPE_THRESHOLD and
            context.mann_kendall_confidence >= self.MANN_KENDALL_CONFIDENCE_THRESHOLD and
            context.mann_kendall_trend == "decreasing"
        )

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Steeper negative slope = higher priority
        - Higher statistical confidence = higher priority
        - Already dry conditions = higher priority
        """
        base = 60

        # Steeper slope = higher priority
        if context.sen_slope_per_month is not None:
            slope_factor = abs(context.sen_slope_per_month) * 50
            base += min(20, slope_factor)

        # Higher confidence = higher priority
        if context.mann_kendall_confidence is not None:
            if context.mann_kendall_confidence > 95:
                base += 10
            elif context.mann_kendall_confidence > 90:
                base += 5

        # Already in drought conditions
        spi = context.spi_6 if context.spi_6 is not None else 0
        if spi < -1.0:
            base += 10

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        slope = context.sen_slope_per_month or 0
        confidence = context.mann_kendall_confidence or 0
        projected_3m = slope * 3

        return (
            f"[TENDENCIA CONFIRMADA] Sen slope = {slope:.3f} SPI/mes "
            f"(Mann-Kendall {confidence:.0f}% confianza). "
            f"Proyección: condiciones empeorarán {abs(projected_3m):.2f} unidades SPI en 3 meses. "
            f"Iniciar medidas preventivas antes del deterioro proyectado."
        )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        slope = context.sen_slope_per_month or 0
        confidence = context.mann_kendall_confidence or 0

        # Steeper slopes warrant more aggressive restrictions
        if slope < -0.2:
            restriction_level = "mandatory"
        elif slope < -0.15:
            restriction_level = "recommended"
        else:
            restriction_level = "voluntary"

        return {
            "sen_slope": slope,
            "mann_kendall_confidence": confidence,
            "projected_spi_change_3m": slope * 3,
            "projected_spi_change_6m": slope * 6,
            "restriction_level": restriction_level,
            "planning_horizon_months": 6,
        }
