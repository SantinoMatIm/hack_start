"""Scenario builder for act vs. no-act simulations."""

from typing import Optional
from dataclasses import dataclass, field
import uuid

from src.config.constants import Trend, RiskLevel, classify_risk_level
from src.risk_engine.critical_estimator import CriticalEstimator


@dataclass
class ScenarioProjection:
    """Projection result for a scenario."""

    scenario_type: str  # 'no_action' or 'with_action'
    projection_days: int
    starting_spi: float
    ending_spi: float
    starting_risk_level: RiskLevel
    ending_risk_level: RiskLevel
    days_to_critical: Optional[int]
    trajectory: list[dict] = field(default_factory=list)


@dataclass
class ActionEffect:
    """Effect of an action on SPI trajectory."""

    action_code: str
    days_gained: float
    spi_improvement: float
    activation_day: int = 0


class ScenarioBuilder:
    """
    Build and simulate scenarios for drought response.

    Compares:
    - No-action scenario: Natural SPI trajectory
    - With-action scenario: SPI trajectory with interventions
    """

    def __init__(
        self,
        critical_estimator: Optional[CriticalEstimator] = None,
    ):
        self.critical_est = critical_estimator or CriticalEstimator()

    def build_no_action_scenario(
        self,
        current_spi: float,
        trend: Trend,
        projection_days: int = 90,
    ) -> ScenarioProjection:
        """
        Build no-action scenario projection.

        Projects SPI trajectory without any interventions.

        Args:
            current_spi: Current SPI-6 value
            trend: Current trend
            projection_days: Days to project

        Returns:
            ScenarioProjection for no-action case
        """
        trajectory = self.critical_est.project_spi_trajectory(
            current_spi=current_spi,
            trend=trend,
            days=projection_days,
        )

        ending_spi = trajectory[-1]["projected_spi"] if trajectory else current_spi

        days_to_critical = self.critical_est.estimate_days_to_critical(
            current_spi=current_spi,
            trend=trend,
        )

        return ScenarioProjection(
            scenario_type="no_action",
            projection_days=projection_days,
            starting_spi=current_spi,
            ending_spi=ending_spi,
            starting_risk_level=classify_risk_level(current_spi),
            ending_risk_level=classify_risk_level(ending_spi),
            days_to_critical=days_to_critical,
            trajectory=trajectory,
        )

    def calculate_action_effects(
        self,
        actions: list[dict],
    ) -> list[ActionEffect]:
        """
        Calculate effects of actions on SPI trajectory.

        Args:
            actions: List of action dictionaries with expected_effect

        Returns:
            List of ActionEffect objects
        """
        effects = []

        for action in actions:
            expected = action.get("expected_effect", {})
            days_gained = expected.get("days_gained", 0)

            # Convert days gained to SPI improvement
            # Approximation: 1 day ~ 0.02 SPI units
            spi_improvement = days_gained * 0.02

            effect = ActionEffect(
                action_code=action.get("action_code", "unknown"),
                days_gained=days_gained,
                spi_improvement=spi_improvement,
                activation_day=action.get("urgency_days", 0),
            )
            effects.append(effect)

        return effects

    def build_with_action_scenario(
        self,
        current_spi: float,
        trend: Trend,
        actions: list[dict],
        projection_days: int = 90,
    ) -> ScenarioProjection:
        """
        Build scenario with action interventions.

        Projects SPI trajectory with effects of actions applied.

        Args:
            current_spi: Current SPI-6 value
            trend: Current trend
            actions: List of actions to apply
            projection_days: Days to project

        Returns:
            ScenarioProjection for with-action case
        """
        # Calculate action effects
        effects = self.calculate_action_effects(actions)

        # Total SPI improvement from all actions
        total_spi_improvement = sum(e.spi_improvement for e in effects)
        total_days_gained = sum(e.days_gained for e in effects)

        # Get base trajectory
        base_trajectory = self.critical_est.project_spi_trajectory(
            current_spi=current_spi,
            trend=trend,
            days=projection_days,
        )

        # Apply action effects to trajectory
        modified_trajectory = self._apply_effects_to_trajectory(
            base_trajectory=base_trajectory,
            effects=effects,
            total_improvement=total_spi_improvement,
        )

        ending_spi = modified_trajectory[-1]["projected_spi"] if modified_trajectory else current_spi

        # Estimate new days to critical
        # Account for action effects
        base_days = self.critical_est.estimate_days_to_critical(
            current_spi=current_spi,
            trend=trend,
        )

        if base_days is not None:
            days_to_critical = base_days + int(total_days_gained)
        else:
            days_to_critical = None

        return ScenarioProjection(
            scenario_type="with_action",
            projection_days=projection_days,
            starting_spi=current_spi,
            ending_spi=ending_spi,
            starting_risk_level=classify_risk_level(current_spi),
            ending_risk_level=classify_risk_level(ending_spi),
            days_to_critical=days_to_critical,
            trajectory=modified_trajectory,
        )

    def _apply_effects_to_trajectory(
        self,
        base_trajectory: list[dict],
        effects: list[ActionEffect],
        total_improvement: float,
    ) -> list[dict]:
        """
        Apply action effects to base trajectory.

        Effects are gradually applied based on action activation days.
        """
        if not base_trajectory or total_improvement == 0:
            return base_trajectory

        modified = []

        # Calculate cumulative improvement over time
        for point in base_trajectory:
            day = point["day"]
            base_spi = point["projected_spi"]

            # Calculate how much improvement has been realized by this day
            realized_improvement = 0
            for effect in effects:
                if day >= effect.activation_day:
                    # Improvement ramps up over 14 days after activation
                    days_since_activation = day - effect.activation_day
                    ramp_factor = min(1.0, days_since_activation / 14)
                    realized_improvement += effect.spi_improvement * ramp_factor

            # Apply improvement (makes SPI less negative)
            improved_spi = base_spi + realized_improvement

            modified.append({
                "day": day,
                "projected_spi": round(improved_spi, 3),
                "risk_level": self._classify_spi(improved_spi),
                "improvement_applied": round(realized_improvement, 3),
            })

        return modified

    def _classify_spi(self, spi: float) -> str:
        """Quick SPI classification."""
        if spi > -0.5:
            return "LOW"
        elif spi > -1.0:
            return "MEDIUM"
        elif spi > -1.5:
            return "HIGH"
        else:
            return "CRITICAL"

    def compare_scenarios(
        self,
        current_spi: float,
        trend: Trend,
        actions: list[dict],
        projection_days: int = 90,
    ) -> dict:
        """
        Compare no-action and with-action scenarios.

        Args:
            current_spi: Current SPI
            trend: Current trend
            actions: Actions to apply
            projection_days: Days to project

        Returns:
            Dictionary with both scenarios and comparison
        """
        no_action = self.build_no_action_scenario(
            current_spi=current_spi,
            trend=trend,
            projection_days=projection_days,
        )

        with_action = self.build_with_action_scenario(
            current_spi=current_spi,
            trend=trend,
            actions=actions,
            projection_days=projection_days,
        )

        # Calculate deltas
        days_gained = 0
        if no_action.days_to_critical is not None and with_action.days_to_critical is not None:
            days_gained = with_action.days_to_critical - no_action.days_to_critical
        elif no_action.days_to_critical is not None:
            # With action avoids critical entirely
            days_gained = projection_days - no_action.days_to_critical

        spi_improvement = with_action.ending_spi - no_action.ending_spi

        return {
            "no_action": {
                "ending_spi": no_action.ending_spi,
                "ending_risk_level": no_action.ending_risk_level.value,
                "days_to_critical": no_action.days_to_critical,
                "trajectory": no_action.trajectory,
            },
            "with_action": {
                "ending_spi": with_action.ending_spi,
                "ending_risk_level": with_action.ending_risk_level.value,
                "days_to_critical": with_action.days_to_critical,
                "trajectory": with_action.trajectory,
            },
            "comparison": {
                "days_gained": days_gained,
                "spi_improvement": round(spi_improvement, 3),
                "risk_level_change": f"{no_action.ending_risk_level.value} -> {with_action.ending_risk_level.value}",
                "actions_count": len(actions),
            },
        }
