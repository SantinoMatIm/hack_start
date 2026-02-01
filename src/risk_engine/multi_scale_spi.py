"""Multi-scale SPI calculator for computing SPI across multiple time scales."""

from typing import Optional
import pandas as pd

from src.risk_engine.spi_calculator import SPICalculator


class MultiScaleSPICalculator:
    """
    Calculate SPI across multiple time scales (1, 3, 6, 12, 24, 48 months).

    This is essential for the new heuristics which require analyzing drought
    conditions at different temporal resolutions:
    - SPI-1/3: Meteorological drought (short-term)
    - SPI-6: Agricultural drought (medium-term)
    - SPI-12/24: Hydrological drought (long-term)
    - SPI-48: Multi-year drought patterns
    """

    SCALES = [1, 3, 6, 12, 24, 48]

    def __init__(self):
        """Initialize calculators for each scale."""
        self._calculators: dict[int, SPICalculator] = {}
        for scale in self.SCALES:
            min_years = max(5, scale // 12 + 5)
            self._calculators[scale] = SPICalculator(
                aggregation_months=scale,
                min_years=min_years
            )

    def calculate_all_scales(
        self,
        daily_precip: pd.DataFrame
    ) -> dict[int, pd.DataFrame]:
        """
        Calculate SPI for all time scales.

        Args:
            daily_precip: DataFrame with 'date' and 'precipitation_mm' columns

        Returns:
            Dictionary mapping scale (months) to DataFrame with SPI series
        """
        results = {}
        for scale, calc in self._calculators.items():
            try:
                results[scale] = calc.calculate_spi(daily_precip)
            except ValueError:
                results[scale] = pd.DataFrame()
        return results

    def get_current_multi_spi(
        self,
        daily_precip: pd.DataFrame
    ) -> dict[str, Optional[float]]:
        """
        Get current (most recent) SPI values for all scales.

        Args:
            daily_precip: DataFrame with precipitation data

        Returns:
            Dictionary with keys like 'spi_1', 'spi_3', etc.
        """
        all_spi = self.calculate_all_scales(daily_precip)
        current = {}
        for scale, df in all_spi.items():
            key = f"spi_{scale}"
            if not df.empty:
                current[key] = float(df.iloc[-1]["spi"])
            else:
                current[key] = None
        return current

    def get_spi_history(
        self,
        daily_precip: pd.DataFrame,
        scale: int,
        months_back: int = 12
    ) -> list[float]:
        """
        Get historical SPI values for a specific scale.

        Args:
            daily_precip: Precipitation data
            scale: SPI scale (1, 3, 6, 12, 24, 48)
            months_back: Number of months of history to return

        Returns:
            List of SPI values (most recent last)
        """
        if scale not in self._calculators:
            return []

        try:
            df = self._calculators[scale].calculate_spi(daily_precip)
            if df.empty:
                return []
            return df.tail(months_back)["spi"].tolist()
        except ValueError:
            return []

    def get_scale_differential(
        self,
        daily_precip: pd.DataFrame,
        short_scale: int = 1,
        long_scale: int = 12
    ) -> Optional[float]:
        """
        Calculate differential between short-term and long-term SPI.

        Used for H9 (Green Drought Paradox) to detect false recovery.

        Args:
            daily_precip: Precipitation data
            short_scale: Short-term SPI scale (default 1)
            long_scale: Long-term SPI scale (default 12)

        Returns:
            Absolute difference |SPI_short - SPI_long| or None if unavailable
        """
        current = self.get_current_multi_spi(daily_precip)
        short_spi = current.get(f"spi_{short_scale}")
        long_spi = current.get(f"spi_{long_scale}")

        if short_spi is None or long_spi is None:
            return None

        return abs(short_spi - long_spi)

    def check_all_scales_positive(
        self,
        daily_precip: pd.DataFrame,
        scales: list[int] = None
    ) -> bool:
        """
        Check if all specified scales have positive SPI.

        Used for H15 (Step-Down Recovery) to confirm recovery.

        Args:
            daily_precip: Precipitation data
            scales: Scales to check (default [3, 6, 12])

        Returns:
            True if all scales are positive
        """
        scales = scales or [3, 6, 12]
        current = self.get_current_multi_spi(daily_precip)

        for scale in scales:
            spi = current.get(f"spi_{scale}")
            if spi is None or spi <= 0:
                return False

        return True

    def count_consecutive_positive_months(
        self,
        daily_precip: pd.DataFrame,
        scales: list[int] = None
    ) -> int:
        """
        Count consecutive months where all scales are positive.

        Args:
            daily_precip: Precipitation data
            scales: Scales to check (default [3, 6, 12])

        Returns:
            Number of consecutive months with all positive
        """
        scales = scales or [3, 6, 12]
        all_spi = self.calculate_all_scales(daily_precip)

        min_length = min(
            len(all_spi.get(s, pd.DataFrame()))
            for s in scales
        )

        if min_length == 0:
            return 0

        count = 0
        for i in range(min_length - 1, -1, -1):
            all_positive = True
            for scale in scales:
                df = all_spi.get(scale, pd.DataFrame())
                if df.empty or df.iloc[i]["spi"] <= 0:
                    all_positive = False
                    break
            if all_positive:
                count += 1
            else:
                break

        return count
