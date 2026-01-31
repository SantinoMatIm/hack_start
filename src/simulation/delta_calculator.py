"""Delta calculator for comparing scenario outcomes."""

from typing import Optional
from dataclasses import dataclass
import uuid

from sqlalchemy.orm import Session

from src.config.constants import Trend, RiskLevel, classify_risk_level
from src.db.models import Simulation, RiskSnapshot
from src.simulation.scenario_builder import ScenarioBuilder, ScenarioProjection


@dataclass
class ScenarioDelta:
    """Delta between two scenarios."""

    days_gained: int
    spi_improvement: float
    risk_level_improvement: int  # Number of levels improved
    reaches_critical_no_action: bool
    reaches_critical_with_action: bool
    critical_delayed_by: Optional[int]  # Days critical is delayed


class DeltaCalculator:
    """
    Calculate deltas between act and no-act scenarios.

    Provides auditable, numeric comparisons.
    """

    def __init__(self, session: Optional[Session] = None):
        self.session = session
        self.scenario_builder = ScenarioBuilder()

    def calculate_delta(
        self,
        no_action: ScenarioProjection,
        with_action: ScenarioProjection,
    ) -> ScenarioDelta:
        """
        Calculate delta between two scenarios.

        Args:
            no_action: No-action scenario projection
            with_action: With-action scenario projection

        Returns:
            ScenarioDelta with all comparison metrics
        """
        # Days gained
        days_gained = 0
        if no_action.days_to_critical is not None:
            if with_action.days_to_critical is not None:
                days_gained = with_action.days_to_critical - no_action.days_to_critical
            else:
                # With action avoids critical
                days_gained = no_action.projection_days

        # SPI improvement
        spi_improvement = with_action.ending_spi - no_action.ending_spi

        # Risk level improvement
        risk_order = {
            RiskLevel.CRITICAL: 0,
            RiskLevel.HIGH: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.LOW: 3,
        }
        no_action_level = risk_order.get(no_action.ending_risk_level, 0)
        with_action_level = risk_order.get(with_action.ending_risk_level, 0)
        risk_improvement = with_action_level - no_action_level

        # Critical threshold analysis
        critical_threshold = -2.0
        reaches_critical_no = no_action.ending_spi <= critical_threshold
        reaches_critical_with = with_action.ending_spi <= critical_threshold

        critical_delayed = None
        if no_action.days_to_critical is not None and with_action.days_to_critical is not None:
            critical_delayed = with_action.days_to_critical - no_action.days_to_critical

        return ScenarioDelta(
            days_gained=days_gained,
            spi_improvement=spi_improvement,
            risk_level_improvement=risk_improvement,
            reaches_critical_no_action=reaches_critical_no,
            reaches_critical_with_action=reaches_critical_with,
            critical_delayed_by=critical_delayed,
        )

    def simulate_and_store(
        self,
        zone_id: uuid.UUID,
        snapshot_id: uuid.UUID,
        current_spi: float,
        trend: Trend,
        actions: list[dict],
        projection_days: int = 90,
    ) -> dict:
        """
        Run simulation and store results in database.

        Args:
            zone_id: Zone UUID
            snapshot_id: Input risk snapshot UUID
            current_spi: Current SPI
            trend: Current trend
            actions: Actions to simulate
            projection_days: Days to project

        Returns:
            Simulation results with IDs
        """
        # Build scenarios
        comparison = self.scenario_builder.compare_scenarios(
            current_spi=current_spi,
            trend=trend,
            actions=actions,
            projection_days=projection_days,
        )

        result = {
            "zone_id": str(zone_id),
            "input_snapshot_id": str(snapshot_id),
            "comparison": comparison["comparison"],
        }

        # Store simulations if session available
        if self.session:
            # No-action simulation
            no_action_sim = Simulation(
                zone_id=zone_id,
                scenario_type="no_action",
                input_snapshot_id=snapshot_id,
                action_instance_ids=None,
                future_spi=comparison["no_action"]["ending_spi"],
                future_risk_level=comparison["no_action"]["ending_risk_level"],
                days_to_critical=comparison["no_action"]["days_to_critical"],
                projection_days=projection_days,
            )
            self.session.add(no_action_sim)

            # With-action simulation
            action_ids = [a.get("action_instance_id") for a in actions if a.get("action_instance_id")]
            with_action_sim = Simulation(
                zone_id=zone_id,
                scenario_type="with_action",
                input_snapshot_id=snapshot_id,
                action_instance_ids=action_ids if action_ids else None,
                future_spi=comparison["with_action"]["ending_spi"],
                future_risk_level=comparison["with_action"]["ending_risk_level"],
                days_to_critical=comparison["with_action"]["days_to_critical"],
                projection_days=projection_days,
            )
            self.session.add(with_action_sim)

            self.session.commit()

            result["no_action_simulation_id"] = str(no_action_sim.id)
            result["with_action_simulation_id"] = str(with_action_sim.id)

        result["no_action"] = comparison["no_action"]
        result["with_action"] = comparison["with_action"]

        return result

    def get_simulation_history(
        self,
        zone_id: uuid.UUID,
        limit: int = 10,
    ) -> list[dict]:
        """Get recent simulations for a zone."""
        if not self.session:
            return []

        simulations = (
            self.session.query(Simulation)
            .filter(Simulation.zone_id == zone_id)
            .order_by(Simulation.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": str(s.id),
                "scenario_type": s.scenario_type,
                "future_spi": s.future_spi,
                "future_risk_level": s.future_risk_level,
                "days_to_critical": s.days_to_critical,
                "projection_days": s.projection_days,
                "created_at": s.created_at.isoformat(),
            }
            for s in simulations
        ]

    def format_delta_summary(self, delta: ScenarioDelta) -> str:
        """
        Format delta as human-readable summary.

        Args:
            delta: ScenarioDelta to format

        Returns:
            Formatted summary string
        """
        lines = []

        # Days gained
        if delta.days_gained > 0:
            lines.append(f"✓ Gains {delta.days_gained} days before critical threshold")
        elif delta.days_gained < 0:
            lines.append(f"⚠ Loses {abs(delta.days_gained)} days (review parameters)")
        else:
            lines.append("→ No change in days to critical")

        # SPI improvement
        if delta.spi_improvement > 0:
            lines.append(f"✓ SPI improves by +{delta.spi_improvement:.2f}")
        elif delta.spi_improvement < 0:
            lines.append(f"⚠ SPI worsens by {delta.spi_improvement:.2f}")

        # Risk level
        if delta.risk_level_improvement > 0:
            lines.append(f"✓ Risk level improves by {delta.risk_level_improvement} level(s)")
        elif delta.risk_level_improvement < 0:
            lines.append(f"⚠ Risk level worsens")

        # Critical analysis
        if delta.reaches_critical_no_action and not delta.reaches_critical_with_action:
            lines.append("✓ Actions PREVENT reaching critical threshold")
        elif delta.reaches_critical_no_action and delta.reaches_critical_with_action:
            if delta.critical_delayed_by and delta.critical_delayed_by > 0:
                lines.append(f"⚠ Critical still reached, but delayed by {delta.critical_delayed_by} days")
            else:
                lines.append("⚠ Critical threshold still reached")

        return "\n".join(lines)
