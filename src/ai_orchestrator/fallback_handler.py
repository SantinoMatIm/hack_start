"""Fallback handler for when AI is unavailable."""

from typing import Optional

from src.config.constants import Trend, FALLBACK_PERCENTILES


class FallbackHandler:
    """
    Handle fallback parameter generation when AI is unavailable.

    Uses trend-based percentile selection:
    - WORSENING: Use 75th percentile (more aggressive)
    - STABLE: Use 50th percentile (default)
    - IMPROVING: Use 25th percentile (conservative)
    """

    def __init__(self):
        pass

    def get_percentile_for_trend(self, trend: Trend) -> float:
        """Get the percentile to use based on trend."""
        return FALLBACK_PERCENTILES.get(trend, 0.5)

    def calculate_parameter_value(
        self,
        param_spec: dict,
        trend: Trend,
    ) -> any:
        """
        Calculate parameter value based on specification and trend.

        Handles different parameter types:
        - Numeric ranges: Use percentile
        - Options list: Select based on severity
        - Boolean: Use trend to decide
        """
        percentile = self.get_percentile_for_trend(trend)

        # Handle numeric ranges
        if "min" in param_spec and "max" in param_spec:
            min_val = param_spec["min"]
            max_val = param_spec["max"]
            value = min_val + (max_val - min_val) * percentile

            # Round integers
            if isinstance(min_val, int) and isinstance(max_val, int):
                value = int(round(value))

            return value

        # Handle options list
        if "options" in param_spec:
            options = param_spec["options"]
            if isinstance(options, list) and options:
                # For worsening, pick more comprehensive options
                if trend == Trend.WORSENING:
                    # Pick last option (often most comprehensive)
                    return options[-1] if len(options) > 0 else options[0]
                elif trend == Trend.IMPROVING:
                    return options[0]
                else:
                    # Middle option
                    mid = len(options) // 2
                    return options[mid]

        # Handle boolean
        if "options" in param_spec and param_spec["options"] == [True, False]:
            return trend == Trend.WORSENING

        # Fall back to default if specified
        if "default" in param_spec:
            return param_spec["default"]

        return None

    def generate_fallback_parameters(
        self,
        parameter_schema: dict,
        trend: Trend,
        default_parameters: Optional[dict] = None,
    ) -> dict:
        """
        Generate fallback parameters when AI is unavailable.

        Args:
            parameter_schema: Schema defining allowed parameters
            trend: Current SPI trend
            default_parameters: Optional defaults from heuristics

        Returns:
            Dictionary of parameter values
        """
        if not parameter_schema:
            return default_parameters or {}

        result = {}

        for param_name, param_spec in parameter_schema.items():
            # Check if we have a default from heuristics
            if default_parameters and param_name in default_parameters:
                result[param_name] = default_parameters[param_name]
                continue

            # Calculate value based on spec and trend
            value = self.calculate_parameter_value(param_spec, trend)
            if value is not None:
                result[param_name] = value
            elif "default" in param_spec:
                result[param_name] = param_spec["default"]

        return result

    def estimate_effect(
        self,
        impact_formula: str,
        parameters: dict,
    ) -> dict:
        """
        Estimate action effect from impact formula.

        Simple parsing of formulas like "5% reduction = +3 days".
        """
        import re

        days_gained = 0.0

        # Try to extract days value
        match = re.search(r'[+]?(\d+(?:\.\d+)?)\s*days', impact_formula.lower())
        if match:
            days_gained = float(match.group(1))

        return {
            "days_gained": days_gained,
            "confidence": "low",  # Fallback estimates have low confidence
            "method": "fallback_heuristic",
        }

    def generate_justification(
        self,
        trend: Trend,
        spi: float,
        days_to_critical: Optional[int],
    ) -> str:
        """Generate a fallback justification string."""
        percentile_pct = int(self.get_percentile_for_trend(trend) * 100)

        trend_desc = {
            Trend.WORSENING: "deteriorating",
            Trend.STABLE: "stable",
            Trend.IMPROVING: "improving",
        }.get(trend, "unknown")

        days_str = f" with {days_to_critical} days to critical threshold" if days_to_critical else ""

        return (
            f"[Auto-generated] Parameters set using {percentile_pct}th percentile defaults "
            f"based on {trend_desc} SPI trend (current: {spi:.2f}){days_str}. "
            f"Review and adjust as needed."
        )
