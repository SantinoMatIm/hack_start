"""Drought magnitude calculator using run theory for cumulative severity."""

from typing import Optional
import numpy as np
import pandas as pd


class DroughtMagnitudeCalculator:
    """
    Calculate cumulative drought magnitude using run theory.

    The magnitude of a drought is the integral of deficit over time:
    M = Σ|SPI| for all months where SPI < threshold

    This captures both intensity AND duration, which is more meaningful
    than point-in-time SPI for economic impact assessment.

    Used by H10 (Drought Magnitude) to trigger scaled responses based
    on historical percentile ranking of current event.
    """

    def __init__(
        self,
        historical_magnitudes: list[float] = None,
        drought_threshold: float = -1.0
    ):
        """
        Initialize calculator.

        Args:
            historical_magnitudes: Pre-computed magnitudes from historical events
            drought_threshold: SPI threshold for drought (default -1.0)
        """
        self.historical_magnitudes = historical_magnitudes or []
        self.drought_threshold = drought_threshold

    def identify_drought_events(
        self,
        spi_series: pd.DataFrame
    ) -> list[dict]:
        """
        Identify distinct drought events (runs) in SPI series.

        A drought event starts when SPI drops below threshold
        and ends when it returns above threshold.

        Args:
            spi_series: DataFrame with 'spi' column

        Returns:
            List of drought events with start, end, duration, magnitude
        """
        if spi_series.empty or "spi" not in spi_series.columns:
            return []

        events = []
        in_drought = False
        current_event = None

        for idx, row in spi_series.iterrows():
            spi = row["spi"]

            if spi < self.drought_threshold:
                if not in_drought:
                    in_drought = True
                    current_event = {
                        "start_idx": idx,
                        "spi_values": [],
                        "min_spi": spi,
                    }
                current_event["spi_values"].append(spi)
                current_event["min_spi"] = min(current_event["min_spi"], spi)
            else:
                if in_drought and current_event:
                    current_event["end_idx"] = idx
                    current_event["duration_months"] = len(current_event["spi_values"])
                    current_event["magnitude"] = sum(
                        abs(v) for v in current_event["spi_values"]
                    )
                    events.append(current_event)
                    current_event = None
                in_drought = False

        if in_drought and current_event:
            current_event["end_idx"] = None
            current_event["duration_months"] = len(current_event["spi_values"])
            current_event["magnitude"] = sum(
                abs(v) for v in current_event["spi_values"]
            )
            current_event["is_ongoing"] = True
            events.append(current_event)

        return events

    def calculate_current_magnitude(
        self,
        spi_series: pd.DataFrame
    ) -> dict:
        """
        Calculate magnitude of current (ongoing) drought event.

        Args:
            spi_series: DataFrame with 'spi' column

        Returns:
            Dictionary with magnitude, duration, and percentile rank
        """
        events = self.identify_drought_events(spi_series)

        if not events:
            return {
                "magnitude": 0.0,
                "duration_months": 0,
                "min_spi": 0.0,
                "percentile_rank": 0.0,
                "is_ongoing": False,
            }

        latest = events[-1]

        is_ongoing = latest.get("is_ongoing", False)

        if not is_ongoing:
            if spi_series.iloc[-1]["spi"] >= self.drought_threshold:
                return {
                    "magnitude": 0.0,
                    "duration_months": 0,
                    "min_spi": 0.0,
                    "percentile_rank": 0.0,
                    "is_ongoing": False,
                }

        magnitude = latest["magnitude"]
        duration = latest["duration_months"]
        min_spi = latest["min_spi"]

        percentile = self._calculate_percentile(magnitude)

        return {
            "magnitude": magnitude,
            "duration_months": duration,
            "min_spi": min_spi,
            "percentile_rank": percentile,
            "is_ongoing": is_ongoing,
        }

    def _calculate_percentile(self, magnitude: float) -> float:
        """
        Calculate percentile rank of magnitude vs historical events.

        Args:
            magnitude: Current drought magnitude

        Returns:
            Percentile rank (0-100)
        """
        if not self.historical_magnitudes:
            if magnitude > 0:
                return 50.0
            return 0.0

        count_below = sum(1 for m in self.historical_magnitudes if m < magnitude)
        percentile = (count_below / len(self.historical_magnitudes)) * 100

        return float(percentile)

    def fit_historical(self, spi_series: pd.DataFrame) -> None:
        """
        Fit calculator with historical drought magnitudes.

        Identifies all historical events and stores their magnitudes
        for percentile calculations.

        Args:
            spi_series: Complete historical SPI series
        """
        events = self.identify_drought_events(spi_series)
        self.historical_magnitudes = [e["magnitude"] for e in events]

    def get_severity_tier(
        self,
        percentile: float
    ) -> str:
        """
        Map percentile to severity tier for response scaling.

        Args:
            percentile: Percentile rank

        Returns:
            Severity tier name
        """
        if percentile >= 90:
            return "extreme"
        elif percentile >= 75:
            return "severe"
        elif percentile >= 50:
            return "moderate"
        elif percentile >= 25:
            return "mild"
        else:
            return "below_average"

    def compare_to_historical_events(
        self,
        current_magnitude: float,
        top_n: int = 5
    ) -> list[dict]:
        """
        Compare current magnitude to top historical events.

        Args:
            current_magnitude: Current drought magnitude
            top_n: Number of historical events to compare

        Returns:
            List of comparisons
        """
        if not self.historical_magnitudes:
            return []

        sorted_hist = sorted(self.historical_magnitudes, reverse=True)
        top_events = sorted_hist[:top_n]

        comparisons = []
        for i, hist_mag in enumerate(top_events):
            comparisons.append({
                "rank": i + 1,
                "historical_magnitude": hist_mag,
                "current_magnitude": current_magnitude,
                "ratio": current_magnitude / hist_mag if hist_mag > 0 else 0,
                "percent_of_historical": (
                    (current_magnitude / hist_mag) * 100
                    if hist_mag > 0 else 0
                ),
            })

        return comparisons

    def get_magnitude_context(
        self,
        spi_series: pd.DataFrame
    ) -> dict:
        """
        Get complete magnitude context for heuristic evaluation.

        Args:
            spi_series: SPI data

        Returns:
            Complete context dictionary for HeuristicContext
        """
        result = self.calculate_current_magnitude(spi_series)

        severity_tier = self.get_severity_tier(result["percentile_rank"])

        return {
            "drought_magnitude": result["magnitude"],
            "magnitude_percentile": result["percentile_rank"],
            "drought_duration_months": result["duration_months"],
            "drought_min_spi": result["min_spi"],
            "drought_is_ongoing": result["is_ongoing"],
            "severity_tier": severity_tier,
        }
