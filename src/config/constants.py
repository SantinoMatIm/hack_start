"""Constants for SPI thresholds, heuristic parameters, and profile weights."""

from enum import Enum
from typing import NamedTuple


class RiskLevel(str, Enum):
    """Risk classification levels based on SPI-6."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Trend(str, Enum):
    """Trend classification for SPI movement."""

    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    WORSENING = "WORSENING"


class Profile(str, Enum):
    """User profile types."""

    GOVERNMENT = "government"
    INDUSTRY = "industry"


# SPI-6 Thresholds for Risk Classification
# Based on standard SPI classification
SPI_THRESHOLDS = {
    RiskLevel.LOW: (-0.5, float("inf")),        # SPI > -0.5
    RiskLevel.MEDIUM: (-1.0, -0.5),             # -1.0 < SPI <= -0.5
    RiskLevel.HIGH: (-1.5, -1.0),               # -1.5 < SPI <= -1.0
    RiskLevel.CRITICAL: (float("-inf"), -1.5),  # SPI <= -1.5
}


def classify_risk_level(spi: float) -> RiskLevel:
    """Classify risk level based on SPI value."""
    if spi > -0.5:
        return RiskLevel.LOW
    elif spi > -1.0:
        return RiskLevel.MEDIUM
    elif spi > -1.5:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


# Trend thresholds (change in SPI over 2 weeks)
TREND_THRESHOLDS = {
    Trend.IMPROVING: 0.1,    # SPI increased by > 0.1
    Trend.STABLE: -0.1,      # SPI changed by -0.1 to 0.1
    Trend.WORSENING: -0.1,   # SPI decreased by > 0.1
}


# Days to critical estimation parameters
DAYS_TO_CRITICAL_PARAMS = {
    "base_decline_rate": 0.02,  # SPI units per day under normal conditions
    "worsening_multiplier": 1.5,
    "improving_multiplier": 0.5,
    "critical_threshold": -2.0,  # SPI value considered critical
}


class HeuristicParams(NamedTuple):
    """Parameters for a heuristic rule."""

    spi_min: float
    spi_max: float
    days_min: int | None
    days_max: int | None
    allowed_trends: tuple[Trend, ...]
    impact_days_per_unit: float
    base_unit: float


# Heuristic activation parameters
HEURISTIC_PARAMS = {
    "H1_INDUSTRIAL_REDUCTION": HeuristicParams(
        spi_min=-1.5,
        spi_max=-1.0,
        days_min=45,
        days_max=None,
        allowed_trends=(Trend.STABLE, Trend.WORSENING),
        impact_days_per_unit=0.6,  # +3 days per 5% reduction
        base_unit=5.0,
    ),
    "H2_PRESSURE_MANAGEMENT": HeuristicParams(
        spi_min=-1.8,
        spi_max=-1.2,
        days_min=30,
        days_max=45,
        allowed_trends=(Trend.WORSENING,),
        impact_days_per_unit=0.4,  # +4 days per 10% pressure reduction
        base_unit=10.0,
    ),
    "H3_PUBLIC_COMMUNICATION": HeuristicParams(
        spi_min=-2.0,
        spi_max=-1.0,
        days_min=30,
        days_max=None,
        allowed_trends=(Trend.WORSENING,),
        impact_days_per_unit=0.67,  # +2 days per 3% reduction
        base_unit=3.0,
    ),
    "H4_NONESSENTIAL_RESTRICTION": HeuristicParams(
        spi_min=float("-inf"),
        spi_max=-1.8,
        days_min=None,
        days_max=30,
        allowed_trends=(Trend.WORSENING,),
        impact_days_per_unit=1.3,  # +1.3 days per 1% removed
        base_unit=1.0,
    ),
    "H5_SOURCE_REALLOCATION": HeuristicParams(
        spi_min=float("-inf"),
        spi_max=-2.0,
        days_min=15,
        days_max=30,
        allowed_trends=(Trend.STABLE, Trend.WORSENING),
        impact_days_per_unit=1.0,  # +5 days per 5% increase
        base_unit=5.0,
    ),
    "H6_SEVERITY_ESCALATION": HeuristicParams(
        spi_min=float("-inf"),
        spi_max=float("inf"),
        days_min=None,
        days_max=None,
        allowed_trends=(Trend.WORSENING,),
        impact_days_per_unit=0.8,  # multiplier for combined effects
        base_unit=1.0,
    ),
}


# Profile weights for action prioritization
# Higher weight = higher priority for that profile
PROFILE_WEIGHTS = {
    Profile.GOVERNMENT: {
        "public_health": 1.5,
        "economic_impact": 1.0,
        "implementation_speed": 1.2,
        "political_feasibility": 1.3,
        "equity": 1.4,
    },
    Profile.INDUSTRY: {
        "public_health": 1.0,
        "economic_impact": 1.5,
        "implementation_speed": 1.4,
        "political_feasibility": 0.8,
        "equity": 0.9,
    },
}


# Pilot zones configuration
PILOT_ZONES = {
    "cdmx": {
        "name": "Mexico City",
        "latitude": 19.4326,
        "longitude": -99.1332,
        "population": 21_900_000,
        "water_consumption_mld": 2600,  # Million liters per day
    },
    "monterrey": {
        "name": "Monterrey",
        "latitude": 25.6866,
        "longitude": -100.3161,
        "population": 5_300_000,
        "water_consumption_mld": 850,
    },
}


# SPI calculation parameters
SPI_PARAMS = {
    "aggregation_months": 6,  # SPI-6
    "min_years_required": 30,
    "gamma_fit_method": "mle",  # Maximum likelihood estimation
}


# AI Orchestrator parameters
AI_PARAMS = {
    "model": "gpt-4o-mini",
    "max_tokens": 1000,
    "temperature": 0.3,
    "max_retries": 3,
    "retry_delay_seconds": 1,
}


# Fallback parameter percentiles based on trend
FALLBACK_PERCENTILES = {
    Trend.WORSENING: 0.75,  # 75th percentile (more aggressive)
    Trend.STABLE: 0.50,     # 50th percentile (default)
    Trend.IMPROVING: 0.25,  # 25th percentile (conservative)
}
