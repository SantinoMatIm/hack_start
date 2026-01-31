"""Days-to-critical estimator based on SPI trajectory."""

from typing import Optional
import pandas as pd
import numpy as np

from src.config.constants import Trend, DAYS_TO_CRITICAL_PARAMS


class CriticalEstimator:
    """
    Estimate days until SPI reaches critical threshold.

    Uses current SPI, trend, and historical rate of change to project
    when conditions will reach critical level (SPI < -2.0).
    """

    def __init__(
        self,
        critical_threshold: float = -2.0,
        base_decline_rate: float = 0.02,
        worsening_multiplier: float = 1.5,
        improving_multiplier: float = 0.5,
    ):
        """
        Initialize estimator.

        Args:
            critical_threshold: SPI value considered critical
            base_decline_rate: Base SPI decline per day
            worsening_multiplier: Multiplier for worsening trend
            improving_multiplier: Multiplier for improving trend
        """
        self.critical_threshold = critical_threshold
        self.base_decline_rate = base_decline_rate
        self.worsening_multiplier = worsening_multiplier
        self.improving_multiplier = improving_multiplier

    def estimate_days_to_critical(
        self,
        current_spi: float,
        trend: Trend,
        spi_series: Optional[pd.DataFrame] = None,
    ) -> Optional[int]:
        """
        Estimate days until critical threshold is reached.

        Args:
            current_spi: Current SPI-6 value
            trend: Current trend classification
            spi_series: Optional historical SPI data for rate calculation

        Returns:
            Estimated days to critical, or None if already critical or improving
        """
        # Already at or below critical
        if current_spi <= self.critical_threshold:
            return 0

        # If improving significantly, may never reach critical
        if trend == Trend.IMPROVING and current_spi > -1.0:
            return None

        # Calculate effective decline rate
        decline_rate = self._calculate_decline_rate(trend, spi_series)

        if decline_rate <= 0:
            # No decline expected
            return None

        # Calculate days to reach critical
        spi_gap = current_spi - self.critical_threshold
        days = int(spi_gap / decline_rate)

        # Cap at reasonable maximum
        return min(days, 365)

    def _calculate_decline_rate(
        self,
        trend: Trend,
        spi_series: Optional[pd.DataFrame] = None,
    ) -> float:
        """
        Calculate effective daily SPI decline rate.

        Combines base rate with trend multiplier and historical data.
        """
        # Start with base rate
        base_rate = self.base_decline_rate

        # Apply trend multiplier
        if trend == Trend.WORSENING:
            rate = base_rate * self.worsening_multiplier
        elif trend == Trend.IMPROVING:
            rate = base_rate * self.improving_multiplier
        else:  # STABLE
            rate = base_rate

        # Adjust based on historical rate if available
        if spi_series is not None and len(spi_series) >= 3:
            historical_rate = self._calculate_historical_rate(spi_series)
            if historical_rate > 0:
                # Weight historical rate more heavily
                rate = (rate + historical_rate * 2) / 3

        return rate

    def _calculate_historical_rate(
        self,
        spi_series: pd.DataFrame,
    ) -> float:
        """
        Calculate average daily decline rate from historical data.

        Uses monthly SPI changes converted to daily rate.
        """
        if len(spi_series) < 2:
            return 0.0

        # Calculate monthly changes
        monthly_changes = spi_series["spi"].diff().dropna()

        # Only consider declines (negative changes)
        declines = monthly_changes[monthly_changes < 0]

        if declines.empty:
            return 0.0

        # Average monthly decline, converted to daily
        avg_monthly_decline = abs(declines.mean())
        daily_rate = avg_monthly_decline / 30

        return daily_rate

    def project_spi_trajectory(
        self,
        current_spi: float,
        trend: Trend,
        days: int = 90,
        spi_series: Optional[pd.DataFrame] = None,
    ) -> list[dict]:
        """
        Project SPI trajectory for future days.

        Args:
            current_spi: Current SPI value
            trend: Current trend
            days: Days to project
            spi_series: Optional historical data

        Returns:
            List of daily projections with day and projected_spi
        """
        decline_rate = self._calculate_decline_rate(trend, spi_series)

        projections = []
        spi = current_spi

        for day in range(days + 1):
            projections.append({
                "day": day,
                "projected_spi": round(spi, 3),
                "risk_level": self._classify_spi(spi),
            })

            # Apply daily decline
            spi -= decline_rate

            # SPI has a practical floor
            spi = max(spi, -4.0)

        return projections

    def _classify_spi(self, spi: float) -> str:
        """Quick SPI classification for projections."""
        if spi > -0.5:
            return "LOW"
        elif spi > -1.0:
            return "MEDIUM"
        elif spi > -1.5:
            return "HIGH"
        else:
            return "CRITICAL"

    def get_critical_probability(
        self,
        current_spi: float,
        trend: Trend,
        days_ahead: int = 30,
    ) -> float:
        """
        Estimate probability of reaching critical within N days.

        Simple heuristic based on current conditions.

        Args:
            current_spi: Current SPI
            trend: Current trend
            days_ahead: Planning horizon

        Returns:
            Probability estimate (0-1)
        """
        if current_spi <= self.critical_threshold:
            return 1.0

        days_to_critical = self.estimate_days_to_critical(current_spi, trend)

        if days_to_critical is None:
            return 0.05  # Small baseline probability

        if days_to_critical <= days_ahead:
            return 0.9  # High probability

        # Linear interpolation
        ratio = days_ahead / days_to_critical
        base_prob = 0.1 + (0.8 * ratio)

        # Adjust for trend
        if trend == Trend.WORSENING:
            base_prob *= 1.2
        elif trend == Trend.IMPROVING:
            base_prob *= 0.5

        return min(1.0, max(0.0, base_prob))
