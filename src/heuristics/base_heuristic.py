"""Base heuristic class and context for action activation rules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from src.config.constants import Trend, RiskLevel, Profile


@dataclass
class HeuristicContext:
    """
    Context data for heuristic evaluation.

    Extended to support the 15 new heuristics based on the technical document
    which require multi-scale SPI, statistical analysis, and additional context.
    """

    # === Core context (required) ===
    risk_level: RiskLevel = RiskLevel.LOW
    trend: Trend = Trend.STABLE
    days_to_critical: Optional[int] = None
    profile: Profile = Profile.GOVERNMENT
    zone_slug: str = ""

    # === Multi-scale SPI values ===
    spi_1: Optional[float] = None
    spi_3: Optional[float] = None
    spi_6: Optional[float] = None
    spi_12: Optional[float] = None
    spi_24: Optional[float] = None
    spi_48: Optional[float] = None

    # === Legacy compatibility ===
    @property
    def spi(self) -> float:
        """Alias for spi_6 for backward compatibility."""
        return self.spi_6 if self.spi_6 is not None else 0.0

    # === H1: Persistence Trigger ===
    spi_3_previous_period: Optional[float] = None
    consecutive_dry_periods: int = 0

    # === H2: Flash Drought Detection ===
    current_spi_category: Optional[int] = None
    spi_category_4_weeks_ago: Optional[int] = None

    # === H3: Seasonality Check ===
    is_dry_season: bool = False
    absolute_precipitation_deficit_mm: Optional[float] = None
    seasonal_deficit_threshold_mm: float = 50.0

    # === H4: Phenological Stress ===
    is_critical_phenological_window: bool = False
    crops_affected: list[str] = field(default_factory=list)
    phenological_stages: list[str] = field(default_factory=list)
    phenological_severity_multiplier: float = 1.0

    # === H5: Trend Prediction (Statistical) ===
    sen_slope_per_month: Optional[float] = None
    mann_kendall_confidence: Optional[float] = None
    mann_kendall_trend: Optional[str] = None

    # === H6: Wet Season Failure ===
    wet_season_average_spi: Optional[float] = None
    wet_season_locked: bool = False

    # === H7: Reservoir Lag ===
    reservoir_storage_pct: Optional[float] = None

    # === H8: Groundwater Proxy ===
    groundwater_level_change_pct: Optional[float] = None

    # === H9: Scale Differential (Green Drought) ===
    scale_differential: Optional[float] = None
    false_recovery_detected: bool = False

    # === H10: Drought Magnitude ===
    drought_magnitude: Optional[float] = None
    magnitude_percentile: Optional[float] = None
    drought_duration_months: int = 0
    drought_min_spi: Optional[float] = None
    severity_tier: Optional[str] = None

    # === H11: Markov Transition ===
    transition_prob_to_severe: Optional[float] = None
    transition_prob_to_extreme: Optional[float] = None
    markov_current_state: Optional[str] = None

    # === H12: Weather Whiplash ===
    recent_wet_to_dry_transition: bool = False
    months_since_wet_period: Optional[int] = None
    volatility_index: Optional[float] = None

    # === H13: Industrial (Cooling Towers) ===
    industrial_coc_current: Optional[float] = None

    # === H14: Infrastructure Defense ===
    demand_capacity_ratio: Optional[float] = None

    # === H15: Step-Down Recovery ===
    all_scales_positive_months: int = 0

    # === Additional optional context ===
    population: Optional[int] = None
    water_consumption_mld: Optional[float] = None
    recent_spi_change: Optional[float] = None
    rapid_deterioration: bool = False


@dataclass
class HeuristicResult:
    """Result of heuristic evaluation."""

    heuristic_id: str
    activated: bool
    applicable_actions: list[str] = field(default_factory=list)
    priority_score: float = 0.0
    justification: str = ""
    parameters: dict = field(default_factory=dict)


class BaseHeuristic(ABC):
    """
    Base class for all heuristic rules.

    Each heuristic defines activation conditions based on SPI, trend,
    and days-to-critical, and specifies which actions from the catalog
    are applicable when activated.

    Extended to support new heuristics that may require:
    - Multi-scale SPI analysis
    - Statistical trend analysis
    - Phenological context
    - Seasonality validation
    - Markov transition probabilities
    """

    # Override in subclasses
    HEURISTIC_ID: str = ""
    APPLICABLE_ACTION_CODES: list[str] = []

    # Legacy configuration (for simple threshold-based heuristics)
    SPI_MIN: float = float("-inf")
    SPI_MAX: float = float("inf")
    DAYS_MIN: Optional[int] = None
    DAYS_MAX: Optional[int] = None
    ALLOWED_TRENDS: tuple[Trend, ...] = (Trend.STABLE, Trend.WORSENING)

    # New heuristic requirements flags
    REQUIRES_MULTI_SCALE_SPI: bool = False
    REQUIRES_STATISTICAL_ANALYSIS: bool = False
    REQUIRES_PHENOLOGY: bool = False
    REQUIRES_SEASONALITY: bool = False
    REQUIRES_MARKOV: bool = False

    def __init__(self):
        self.heuristic_id = self.HEURISTIC_ID

    def check_activation(self, context: HeuristicContext) -> bool:
        """
        Check if heuristic should be activated given the context.

        Override this method in subclasses for custom activation logic.
        Default implementation uses simple SPI range and trend matching.

        Args:
            context: Current risk context

        Returns:
            True if heuristic conditions are met
        """
        # Get SPI value (use spi_6 as default for compatibility)
        spi_value = context.spi_6 if context.spi_6 is not None else context.spi

        # Check SPI range
        if not (self.SPI_MIN <= spi_value <= self.SPI_MAX):
            return False

        # Check trend
        if context.trend not in self.ALLOWED_TRENDS:
            return False

        # Check days to critical
        if context.days_to_critical is not None:
            if self.DAYS_MIN is not None and context.days_to_critical < self.DAYS_MIN:
                return False
            if self.DAYS_MAX is not None and context.days_to_critical > self.DAYS_MAX:
                return False

        return True

    @abstractmethod
    def calculate_priority(self, context: HeuristicContext) -> float:
        """
        Calculate priority score for this heuristic.

        Higher scores = higher priority.

        Args:
            context: Current risk context

        Returns:
            Priority score (0-100)
        """
        pass

    @abstractmethod
    def generate_justification(self, context: HeuristicContext) -> str:
        """
        Generate human-readable justification for activation.

        Args:
            context: Current risk context

        Returns:
            Justification string
        """
        pass

    def get_default_parameters(self, context: HeuristicContext) -> dict:
        """
        Get default parameters for actions based on context.

        Can be overridden by AI orchestrator.

        Args:
            context: Current risk context

        Returns:
            Dictionary of default parameters
        """
        return {}

    def evaluate(self, context: HeuristicContext) -> HeuristicResult:
        """
        Evaluate heuristic and return result.

        Args:
            context: Current risk context

        Returns:
            HeuristicResult with activation status and details
        """
        activated = self.check_activation(context)

        if not activated:
            return HeuristicResult(
                heuristic_id=self.heuristic_id,
                activated=False,
            )

        priority = self.calculate_priority(context)
        justification = self.generate_justification(context)
        parameters = self.get_default_parameters(context)

        return HeuristicResult(
            heuristic_id=self.heuristic_id,
            activated=True,
            applicable_actions=self.APPLICABLE_ACTION_CODES.copy(),
            priority_score=priority,
            justification=justification,
            parameters=parameters,
        )
