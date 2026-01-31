"""SPI-6 (Standardized Precipitation Index) calculator using gamma distribution."""

from typing import Optional
import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import ndtri


class SPICalculator:
    """
    Calculate Standardized Precipitation Index (SPI) using gamma distribution.

    SPI transforms precipitation data into a standardized normal distribution
    where negative values indicate drought conditions:
    - SPI > 0: Above normal precipitation
    - SPI 0 to -0.5: Near normal
    - SPI -0.5 to -1.0: Moderately dry
    - SPI -1.0 to -1.5: Severely dry
    - SPI -1.5 to -2.0: Extremely dry
    - SPI < -2.0: Exceptionally dry
    """

    def __init__(self, aggregation_months: int = 6, min_years: int = 30):
        """
        Initialize SPI calculator.

        Args:
            aggregation_months: Number of months to aggregate (SPI-6 = 6 months)
            min_years: Minimum years of data required for fitting
        """
        self.aggregation_months = aggregation_months
        self.min_years = min_years
        self._gamma_params_cache: dict = {}

    def _aggregate_monthly(self, daily_precip: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate daily precipitation to monthly totals.

        Args:
            daily_precip: DataFrame with 'date' and 'precipitation_mm' columns

        Returns:
            DataFrame with 'year_month', 'year', 'month', 'precipitation_mm' columns
        """
        df = daily_precip.copy()
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["year_month"] = df["date"].dt.to_period("M")

        monthly = df.groupby(["year_month", "year", "month"])["precipitation_mm"].sum().reset_index()
        return monthly.sort_values("year_month")

    def _calculate_rolling_sum(
        self,
        monthly_precip: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate rolling N-month precipitation sums.

        Args:
            monthly_precip: Monthly aggregated precipitation

        Returns:
            DataFrame with rolling sum column added
        """
        df = monthly_precip.copy()
        df = df.sort_values("year_month")

        # Calculate rolling sum
        col_name = f"precip_{self.aggregation_months}m"
        df[col_name] = df["precipitation_mm"].rolling(
            window=self.aggregation_months,
            min_periods=self.aggregation_months,
        ).sum()

        return df.dropna(subset=[col_name])

    def _fit_gamma_for_month(
        self,
        precip_values: np.ndarray,
    ) -> tuple[float, float, float]:
        """
        Fit gamma distribution to precipitation values for a specific month.

        Uses Maximum Likelihood Estimation (MLE).

        Args:
            precip_values: Array of precipitation values for one calendar month

        Returns:
            Tuple of (alpha/shape, beta/scale, probability_of_zero)
        """
        # Handle zeros - calculate probability of zero precipitation
        zeros = precip_values == 0
        prob_zero = zeros.sum() / len(precip_values)

        # Filter non-zero values for gamma fitting
        non_zero = precip_values[~zeros]

        if len(non_zero) < 10:
            # Not enough data, return defaults
            return (1.0, 1.0, prob_zero)

        try:
            # Fit gamma distribution using MLE
            # scipy.stats.gamma uses shape (a), loc, scale parameterization
            shape, loc, scale = stats.gamma.fit(non_zero, floc=0)
            return (shape, scale, prob_zero)
        except Exception:
            # Fallback to method of moments
            mean = np.mean(non_zero)
            var = np.var(non_zero)
            if var > 0:
                scale = var / mean
                shape = mean / scale
                return (shape, scale, prob_zero)
            return (1.0, mean if mean > 0 else 1.0, prob_zero)

    def _gamma_cdf(
        self,
        x: float,
        shape: float,
        scale: float,
        prob_zero: float,
    ) -> float:
        """
        Calculate CDF of mixed gamma distribution (with zero inflation).

        H(x) = q + (1-q) * G(x)
        where q is probability of zero and G is gamma CDF.
        """
        if x <= 0:
            return prob_zero

        gamma_cdf = stats.gamma.cdf(x, shape, scale=scale)
        return prob_zero + (1 - prob_zero) * gamma_cdf

    def _cdf_to_spi(self, cdf_value: float) -> float:
        """
        Convert CDF value to SPI using inverse normal transformation.

        Handles edge cases near 0 and 1.
        """
        # Clamp to avoid infinity
        cdf_clamped = max(0.001, min(0.999, cdf_value))
        return ndtri(cdf_clamped)

    def calculate_spi(
        self,
        daily_precip: pd.DataFrame,
        target_date: Optional[pd.Timestamp] = None,
    ) -> pd.DataFrame:
        """
        Calculate SPI-6 for precipitation timeseries.

        Args:
            daily_precip: DataFrame with 'date' and 'precipitation_mm' columns
            target_date: Optional specific date to calculate SPI for

        Returns:
            DataFrame with SPI values added
        """
        # Aggregate to monthly
        monthly = self._aggregate_monthly(daily_precip)

        # Calculate rolling sums
        rolling = self._calculate_rolling_sum(monthly)

        if rolling.empty:
            raise ValueError(
                f"Insufficient data: Need at least {self.aggregation_months} months"
            )

        # Check minimum years
        years_available = rolling["year"].nunique()
        if years_available < self.min_years:
            print(f"Warning: Only {years_available} years available, "
                  f"recommended minimum is {self.min_years}")

        precip_col = f"precip_{self.aggregation_months}m"
        spi_values = []

        # Calculate SPI for each month separately (fit per calendar month)
        for month in range(1, 13):
            month_data = rolling[rolling["month"] == month].copy()
            if month_data.empty:
                continue

            precip_values = month_data[precip_col].values

            # Fit gamma distribution for this calendar month
            shape, scale, prob_zero = self._fit_gamma_for_month(precip_values)

            # Cache parameters
            self._gamma_params_cache[month] = (shape, scale, prob_zero)

            # Calculate SPI for each value
            for idx, row in month_data.iterrows():
                cdf = self._gamma_cdf(row[precip_col], shape, scale, prob_zero)
                spi = self._cdf_to_spi(cdf)
                spi_values.append({
                    "year_month": row["year_month"],
                    "year": row["year"],
                    "month": row["month"],
                    "precipitation_mm": row["precipitation_mm"],
                    precip_col: row[precip_col],
                    "spi": spi,
                })

        result = pd.DataFrame(spi_values)
        result = result.sort_values("year_month")

        if target_date is not None:
            target_period = pd.Period(target_date, freq="M")
            result = result[result["year_month"] == target_period]

        return result

    def get_current_spi(
        self,
        daily_precip: pd.DataFrame,
    ) -> float:
        """
        Get the most recent SPI-6 value.

        Args:
            daily_precip: DataFrame with precipitation data

        Returns:
            Most recent SPI value
        """
        spi_series = self.calculate_spi(daily_precip)
        if spi_series.empty:
            raise ValueError("Unable to calculate SPI - insufficient data")

        return spi_series.iloc[-1]["spi"]

    def get_spi_series(
        self,
        daily_precip: pd.DataFrame,
        months_back: int = 12,
    ) -> pd.DataFrame:
        """
        Get SPI series for the last N months.

        Args:
            daily_precip: Precipitation data
            months_back: Number of months to return

        Returns:
            DataFrame with recent SPI values
        """
        spi_series = self.calculate_spi(daily_precip)
        return spi_series.tail(months_back)
