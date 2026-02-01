"""Statistical trend analysis using Mann-Kendall test and Sen slope estimator."""

from typing import Optional
import numpy as np
from scipy import stats


class StatisticalTrendAnalyzer:
    """
    Advanced statistical analysis for drought trend detection.

    Implements:
    - Mann-Kendall test: Non-parametric test for monotonic trend
    - Sen slope estimator: Robust median-based slope calculation

    Used by H5 (Trend Prediction) to detect statistically significant
    degradation patterns before they become critical.
    """

    def mann_kendall_test(
        self,
        spi_series: np.ndarray
    ) -> dict:
        """
        Perform Mann-Kendall test for monotonic trend.

        The test is distribution-free and handles ties properly.

        Args:
            spi_series: Array of SPI values in chronological order

        Returns:
            Dictionary with:
            - trend: 'increasing', 'decreasing', or 'no_trend'
            - p_value: Statistical significance
            - confidence_pct: Confidence level (100 * (1 - p_value))
            - z_statistic: Z-score of the test
            - s_statistic: Mann-Kendall S statistic
        """
        n = len(spi_series)
        if n < 4:
            return {
                "trend": "no_trend",
                "p_value": 1.0,
                "confidence_pct": 0.0,
                "z_statistic": 0.0,
                "s_statistic": 0
            }

        # Calculate S statistic
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                diff = spi_series[j] - spi_series[k]
                if diff > 0:
                    s += 1
                elif diff < 0:
                    s -= 1

        # Calculate variance with tie correction
        unique, counts = np.unique(spi_series, return_counts=True)
        g = len(unique)

        if n == g:
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:
            tp = counts[counts > 1]
            var_s = (n * (n - 1) * (2 * n + 5) -
                     np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18

        if var_s <= 0:
            var_s = 1.0

        # Calculate Z-score with continuity correction
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:
            z = 0.0

        # Two-tailed p-value
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

        # Determine trend
        if z > 0 and p_value < 0.1:
            trend = "increasing"
        elif z < 0 and p_value < 0.1:
            trend = "decreasing"
        else:
            trend = "no_trend"

        return {
            "trend": trend,
            "p_value": float(p_value),
            "confidence_pct": float((1 - p_value) * 100),
            "z_statistic": float(z),
            "s_statistic": int(s)
        }

    def sen_slope(
        self,
        spi_series: np.ndarray,
        time_unit_months: int = 1
    ) -> float:
        """
        Calculate Sen's slope estimator (Theil-Sen estimator).

        A robust, non-parametric estimate of the linear trend slope.
        Uses the median of all pairwise slopes.

        Args:
            spi_series: Array of SPI values in chronological order
            time_unit_months: Time unit between observations (default 1 month)

        Returns:
            Slope in SPI units per month (negative = drying trend)
        """
        n = len(spi_series)
        if n < 2:
            return 0.0

        slopes = []
        for i in range(n - 1):
            for j in range(i + 1, n):
                time_diff = (j - i) * time_unit_months
                if time_diff > 0:
                    slope = (spi_series[j] - spi_series[i]) / time_diff
                    slopes.append(slope)

        if not slopes:
            return 0.0

        return float(np.median(slopes))

    def analyze_trend(
        self,
        spi_series: np.ndarray,
        confidence_threshold: float = 90.0
    ) -> dict:
        """
        Complete trend analysis combining Mann-Kendall and Sen slope.

        Args:
            spi_series: Array of SPI values
            confidence_threshold: Minimum confidence for significant trend

        Returns:
            Dictionary with full analysis results including:
            - is_significant: Whether trend is statistically significant
            - is_degrading: Whether trend indicates worsening drought
            - slope_per_month: Sen slope value
            - confidence_pct: Statistical confidence
            - trend_direction: 'increasing', 'decreasing', 'no_trend'
            - projected_change_3m: Projected SPI change over 3 months
        """
        if len(spi_series) < 4:
            return {
                "is_significant": False,
                "is_degrading": False,
                "slope_per_month": 0.0,
                "confidence_pct": 0.0,
                "trend_direction": "no_trend",
                "projected_change_3m": 0.0
            }

        arr = np.array(spi_series)
        mk_result = self.mann_kendall_test(arr)
        slope = self.sen_slope(arr)

        is_significant = mk_result["confidence_pct"] >= confidence_threshold
        is_degrading = is_significant and slope < 0

        return {
            "is_significant": is_significant,
            "is_degrading": is_degrading,
            "slope_per_month": slope,
            "confidence_pct": mk_result["confidence_pct"],
            "trend_direction": mk_result["trend"],
            "projected_change_3m": slope * 3,
            "mann_kendall": mk_result
        }

    def detect_rapid_intensification(
        self,
        spi_series: np.ndarray,
        threshold_slope: float = -0.25,
        window_months: int = 4
    ) -> bool:
        """
        Detect rapid drought intensification (flash drought signal).

        Args:
            spi_series: Array of SPI values
            threshold_slope: Slope threshold for rapid intensification
            window_months: Window to analyze (default 4 weeks/1 month)

        Returns:
            True if rapid intensification detected
        """
        if len(spi_series) < window_months:
            return False

        recent = np.array(spi_series[-window_months:])
        slope = self.sen_slope(recent)

        return slope <= threshold_slope
