"""Base heuristic class and context for action activation rules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from src.config.constants import Trend, RiskLevel, Profile


@dataclass
class HeuristicContext:
    """Context data for heuristic evaluation."""

    spi: float
    risk_level: RiskLevel
    trend: Trend
    days_to_critical: Optional[int]
    profile: Profile
    zone_slug: str

    # Optional additional context
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
    """

    # Override in subclasses
    HEURISTIC_ID: str = ""
    SPI_MIN: float = float("-inf")
    SPI_MAX: float = float("inf")
    DAYS_MIN: Optional[int] = None
    DAYS_MAX: Optional[int] = None
    ALLOWED_TRENDS: tuple[Trend, ...] = (Trend.STABLE, Trend.WORSENING)
    APPLICABLE_ACTION_CODES: list[str] = []

    def __init__(self):
        self.heuristic_id = self.HEURISTIC_ID

    def check_activation(self, context: HeuristicContext) -> bool:
        """
        Check if heuristic should be activated given the context.

        Args:
            context: Current risk context

        Returns:
            True if heuristic conditions are met
        """
        # Check SPI range
        if not (self.SPI_MIN <= context.spi <= self.SPI_MAX):
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
