"""H3: Seasonality Check - Filtro de Falso Positivo Invernal.

Validates drought signals during dry seasons to avoid false alarms
when negative SPI values are normal for the climatological pattern.
"""

from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext
from src.config.constants import Trend


class H3SeasonalityCheck(BaseHeuristic):
    """
    H3: Seasonality Check (Filtro de Falso Positivo Invernal)

    Rationale:
    - In seasonal climates, dry season dryness is normal
    - Negative SPI during dry season may be statistically valid but
      physically meaningless if absolute precipitation is near-zero anyway
    - Users are confused by drought alerts during expected dry periods
    - Absolute deficit validation prevents false positives

    Activation:
    - SPI-6 < -1.0 AND
    - Either: NOT in dry season, OR
    - In dry season AND absolute deficit > threshold (e.g., 50mm)

    Actions:
    - Validated monitoring (signal confirmed as genuine)
    - Seasonal advisory
    """

    HEURISTIC_ID = "H3"
    REQUIRES_SEASONALITY = True

    APPLICABLE_ACTION_CODES = [
        "H3_VALIDATED_MONITORING",
        "H3_SEASONAL_ADVISORY",
    ]

    SPI_THRESHOLD = -1.0

    def check_activation(self, context: HeuristicContext) -> bool:
        """
        Validate drought signal with seasonal context.

        Returns True only if:
        1. Not in dry season and SPI indicates drought, OR
        2. In dry season but absolute deficit confirms physical drought
        """
        spi = context.spi_6 if context.spi_6 is not None else context.spi

        if spi >= self.SPI_THRESHOLD:
            return False

        # Not in dry season - SPI signal is valid
        if not context.is_dry_season:
            return True

        # In dry season - require absolute deficit validation
        if context.absolute_precipitation_deficit_mm is None:
            return False

        return (
            context.absolute_precipitation_deficit_mm >
            context.seasonal_deficit_threshold_mm
        )

    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Priority based on:
        - Deficit magnitude relative to threshold
        - SPI severity
        """
        base = 45

        # Larger absolute deficit = higher priority
        if context.absolute_precipitation_deficit_mm is not None:
            deficit_ratio = (
                context.absolute_precipitation_deficit_mm /
                context.seasonal_deficit_threshold_mm
            )
            base += min(25, deficit_ratio * 10)

        # Lower SPI = higher priority
        spi = context.spi_6 if context.spi_6 is not None else 0
        if spi < -1.5:
            base += 15
        elif spi < -1.2:
            base += 10

        # Worsening trend
        if context.trend == Trend.WORSENING:
            base += 5

        return min(100, base)

    def generate_justification(self, context: HeuristicContext) -> str:
        spi = context.spi_6 if context.spi_6 is not None else 0
        season = "seca" if context.is_dry_season else "húmeda"
        deficit = context.absolute_precipitation_deficit_mm or 0
        threshold = context.seasonal_deficit_threshold_mm

        if context.is_dry_season:
            return (
                f"[SEÑAL VALIDADA] SPI-6 = {spi:.2f} en temporada {season}. "
                f"Déficit absoluto: {deficit:.0f}mm excede umbral de {threshold:.0f}mm. "
                f"Señal de sequía confirmada - no es falso positivo estacional."
            )
        else:
            return (
                f"SPI-6 = {spi:.2f} en temporada {season}. "
                f"Señal de sequía válida sin necesidad de validación estacional."
            )

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        return {
            "validated": True,
            "is_seasonal_false_positive": False,
            "deficit_mm": context.absolute_precipitation_deficit_mm,
            "threshold_mm": context.seasonal_deficit_threshold_mm,
        }
