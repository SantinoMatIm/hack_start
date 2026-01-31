"""Trend analyzer for SPI movement classification."""

from typing import Optional
import pandas as pd
import numpy as np

from src.config.constants import Trend, TREND_THRESHOLDS


class TrendAnalyzer:
    """
    Analyze SPI trends to classify as IMPROVING, STABLE, or WORSENING.

    Uses a 2-week (14-day) comparison window by default.
    """

    def __init__(
        self,
        comparison_window_days: int = 14,
        improving_threshold: float = 0.1,
        worsening_threshold: float = -0.1,
    ):
        """
        Initialize trend analyzer.

        Args:
            comparison_window_days: Days to look back for comparison
            improving_threshold: SPI change threshold for IMPROVING
            worsening_threshold: SPI change threshold for WORSENING
        """
        self.comparison_window_days = comparison_window_days
        self.improving_threshold = improving_threshold
        self.worsening_threshold = worsening_threshold

    def calculate_spi_change(
        self,
        spi_series: pd.DataFrame,
        current_spi: Optional[float] = None,
    ) -> float:
        """
        Calculate SPI change over the comparison window.

        Args:
            spi_series: DataFrame with SPI values (must have 'spi' column)
            current_spi: Optional current SPI value to use

        Returns:
            SPI change value (positive = improving)
        """
        if spi_series.empty or len(spi_series) < 2:
            return 0.0

        # Get current and previous SPI
        current = current_spi if current_spi is not None else spi_series.iloc[-1]["spi"]

        # For monthly SPI, compare to previous month
        # (14 days approximates half a month)
        if len(spi_series) >= 2:
            previous = spi_series.iloc[-2]["spi"]
        else:
            previous = current

        return current - previous

    def classify_trend(
        self,
        spi_series: pd.DataFrame,
        current_spi: Optional[float] = None,
    ) -> Trend:
        """
        Classify the SPI trend.

        Args:
            spi_series: DataFrame with SPI values
            current_spi: Optional current SPI to use

        Returns:
            Trend classification (IMPROVING, STABLE, WORSENING)
        """
        change = self.calculate_spi_change(spi_series, current_spi)

        if change > self.improving_threshold:
            return Trend.IMPROVING
        elif change < self.worsening_threshold:
            return Trend.WORSENING
        else:
            return Trend.STABLE

    def calculate_rate_of_change(
        self,
        spi_series: pd.DataFrame,
        months: int = 3,
    ) -> float:
        """
        Calculate average rate of SPI change over recent months.

        Args:
            spi_series: DataFrame with SPI values
            months: Number of months to analyze

        Returns:
            Average monthly SPI change
        """
        if len(spi_series) < months + 1:
            return 0.0

        recent = spi_series.tail(months + 1)
        changes = recent["spi"].diff().dropna()

        return changes.mean()

    def is_rapid_deterioration(
        self,
        spi_series: pd.DataFrame,
        threshold_pct: float = 20.0,
        weeks: int = 2,
    ) -> bool:
        """
        Check if SPI has dropped rapidly (trigger for H6).

        Args:
            spi_series: DataFrame with SPI values
            threshold_pct: Percentage drop threshold
            weeks: Time window in weeks (approximated as half-months)

        Returns:
            True if rapid deterioration detected
        """
        if len(spi_series) < 2:
            return False

        current = spi_series.iloc[-1]["spi"]
        previous = spi_series.iloc[-2]["spi"]

        # For negative SPI values, calculate percentage change
        # A drop from -1.0 to -1.2 is a 20% worsening
        if previous != 0:
            pct_change = ((current - previous) / abs(previous)) * 100
        else:
            pct_change = 0

        # Negative percentage = worsening (SPI getting more negative)
        return pct_change < -threshold_pct

    def get_trend_summary(
        self,
        spi_series: pd.DataFrame,
        current_spi: Optional[float] = None,
    ) -> dict:
        """
        Get comprehensive trend analysis summary.

        Args:
            spi_series: DataFrame with SPI values
            current_spi: Optional current SPI

        Returns:
            Dictionary with trend metrics
        """
        trend = self.classify_trend(spi_series, current_spi)
        change = self.calculate_spi_change(spi_series, current_spi)
        rate = self.calculate_rate_of_change(spi_series)
        rapid = self.is_rapid_deterioration(spi_series)

        # Calculate recent statistics
        if not spi_series.empty:
            recent_3m = spi_series.tail(3)["spi"]
            min_spi = recent_3m.min()
            max_spi = recent_3m.max()
            avg_spi = recent_3m.mean()
        else:
            min_spi = max_spi = avg_spi = 0.0

        return {
            "trend": trend,
            "spi_change_2w": round(change, 3),
            "monthly_rate": round(rate, 3),
            "rapid_deterioration": rapid,
            "recent_3m_min": round(min_spi, 2),
            "recent_3m_max": round(max_spi, 2),
            "recent_3m_avg": round(avg_spi, 2),
        }
