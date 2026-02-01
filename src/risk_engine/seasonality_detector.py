"""Seasonality detection for validating drought signals in seasonal climates."""

from datetime import date
from typing import Optional
import pandas as pd


class SeasonalityDetector:
    """
    Detect and validate drought signals in context of seasonal climate patterns.

    Used by:
    - H3 (Seasonality Check): Avoid false positives during dry season
    - H6 (Wet Season Failure): Lock restrictions if rainy season fails

    Regions with distinct wet/dry seasons require context-aware interpretation
    of SPI values to avoid alarming during normal dry periods.
    """

    ZONE_SEASONS = {
        "cdmx": {
            "dry": [11, 12, 1, 2, 3, 4, 5],
            "wet": [6, 7, 8, 9, 10],
        },
        "monterrey": {
            "dry": [11, 12, 1, 2, 3, 4, 5],
            "wet": [6, 7, 8, 9, 10],
        },
        "guadalajara": {
            "dry": [11, 12, 1, 2, 3, 4, 5],
            "wet": [6, 7, 8, 9, 10],
        },
        "sonora": {
            "dry": [10, 11, 12, 1, 2, 3, 4, 5],
            "wet": [6, 7, 8, 9],
        },
        "yucatan": {
            "dry": [11, 12, 1, 2, 3, 4],
            "wet": [5, 6, 7, 8, 9, 10],
        },
        "default": {
            "dry": [11, 12, 1, 2, 3, 4],
            "wet": [5, 6, 7, 8, 9, 10],
        },
    }

    DEFAULT_DEFICIT_THRESHOLD_MM = 50.0

    def __init__(
        self,
        zone_slug: str,
        deficit_threshold_mm: float = None
    ):
        """
        Initialize detector for a specific zone.

        Args:
            zone_slug: Zone identifier
            deficit_threshold_mm: Absolute deficit threshold for validation
        """
        self.zone_slug = zone_slug
        self.deficit_threshold_mm = (
            deficit_threshold_mm or self.DEFAULT_DEFICIT_THRESHOLD_MM
        )
        self.seasons = self.ZONE_SEASONS.get(
            zone_slug.lower(),
            self.ZONE_SEASONS["default"]
        )

    def get_current_season(self, ref_date: Optional[date] = None) -> str:
        """
        Determine current season (dry or wet).

        Args:
            ref_date: Reference date (default: today)

        Returns:
            'dry' or 'wet'
        """
        ref_date = ref_date or date.today()
        month = ref_date.month

        return "dry" if month in self.seasons["dry"] else "wet"

    def is_dry_season(self, ref_date: Optional[date] = None) -> bool:
        """Check if currently in dry season."""
        return self.get_current_season(ref_date) == "dry"

    def is_wet_season(self, ref_date: Optional[date] = None) -> bool:
        """Check if currently in wet season."""
        return self.get_current_season(ref_date) == "wet"

    def requires_deficit_validation(
        self,
        spi_value: float,
        ref_date: Optional[date] = None
    ) -> bool:
        """
        Check if SPI signal requires absolute deficit validation.

        H3: During dry season, negative SPI may be normal.
        Validation needed only if actual deficit exceeds physical threshold.

        Args:
            spi_value: Current SPI value
            ref_date: Reference date

        Returns:
            True if deficit validation is required
        """
        if spi_value >= 0:
            return False

        if self.is_dry_season(ref_date) and spi_value < 0:
            return True

        return False

    def validate_drought_signal(
        self,
        spi_value: float,
        absolute_deficit_mm: Optional[float],
        ref_date: Optional[date] = None
    ) -> dict:
        """
        Validate if drought signal is genuine or seasonal noise.

        Args:
            spi_value: SPI value
            absolute_deficit_mm: Actual precipitation deficit in mm
            ref_date: Reference date

        Returns:
            Dictionary with validation results
        """
        is_dry = self.is_dry_season(ref_date)

        if not is_dry:
            return {
                "is_valid_signal": spi_value < -1.0,
                "is_dry_season": False,
                "requires_validation": False,
                "validation_passed": None,
                "reason": "Wet season - SPI signal valid without validation"
            }

        if spi_value >= -1.0:
            return {
                "is_valid_signal": False,
                "is_dry_season": True,
                "requires_validation": False,
                "validation_passed": None,
                "reason": "SPI above threshold, no drought signal"
            }

        if absolute_deficit_mm is None:
            return {
                "is_valid_signal": False,
                "is_dry_season": True,
                "requires_validation": True,
                "validation_passed": False,
                "reason": "Dry season - deficit data required for validation"
            }

        validation_passed = absolute_deficit_mm > self.deficit_threshold_mm

        return {
            "is_valid_signal": validation_passed,
            "is_dry_season": True,
            "requires_validation": True,
            "validation_passed": validation_passed,
            "absolute_deficit_mm": absolute_deficit_mm,
            "threshold_mm": self.deficit_threshold_mm,
            "reason": (
                f"Deficit {absolute_deficit_mm:.0f}mm "
                f"{'exceeds' if validation_passed else 'below'} "
                f"threshold {self.deficit_threshold_mm:.0f}mm"
            )
        }

    def get_wet_season_months(self) -> list[int]:
        """Get list of wet season months for this zone."""
        return self.seasons["wet"]

    def get_wet_season_spi_average(
        self,
        spi_series: pd.DataFrame,
        years_back: int = 1
    ) -> Optional[float]:
        """
        Calculate average SPI for the most recent wet season(s).

        Used by H6 to detect wet season failure.

        Args:
            spi_series: DataFrame with 'month' and 'spi' columns
            years_back: Number of wet seasons to average

        Returns:
            Average SPI or None if insufficient data
        """
        if spi_series.empty:
            return None

        if "month" not in spi_series.columns:
            return None

        wet_months = self.seasons["wet"]
        wet_data = spi_series[spi_series["month"].isin(wet_months)]

        if wet_data.empty:
            return None

        n_months = len(wet_months) * years_back
        recent_wet = wet_data.tail(n_months)

        if recent_wet.empty:
            return None

        return float(recent_wet["spi"].mean())

    def is_wet_season_failed(
        self,
        spi_series: pd.DataFrame,
        failure_threshold: float = -1.0
    ) -> bool:
        """
        Check if wet season has failed (average SPI below threshold).

        Args:
            spi_series: SPI data with 'month' column
            failure_threshold: SPI threshold for failure (default -1.0)

        Returns:
            True if wet season failed
        """
        avg = self.get_wet_season_spi_average(spi_series, years_back=1)
        if avg is None:
            return False
        return avg < failure_threshold

    def calculate_seasonal_deficit(
        self,
        precip_series: pd.DataFrame,
        ref_date: Optional[date] = None
    ) -> Optional[float]:
        """
        Calculate absolute precipitation deficit for current season.

        Args:
            precip_series: DataFrame with 'date', 'precipitation_mm', 'month'
            ref_date: Reference date

        Returns:
            Deficit in mm or None if insufficient data
        """
        if precip_series.empty:
            return None

        ref_date = ref_date or date.today()
        current_year = ref_date.year

        season = self.get_current_season(ref_date)
        season_months = self.seasons[season]

        current_season = precip_series[
            (precip_series["month"].isin(season_months)) &
            (precip_series["year"] == current_year)
        ]

        historical = precip_series[
            (precip_series["month"].isin(season_months)) &
            (precip_series["year"] < current_year)
        ]

        if current_season.empty or historical.empty:
            return None

        current_total = current_season["precipitation_mm"].sum()
        historical_avg = historical.groupby("year")["precipitation_mm"].sum().mean()

        return historical_avg - current_total
