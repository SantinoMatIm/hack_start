"""Economic cost calculator for power infrastructure dependent on water.

Calculates avoided costs when water actions prevent power plant capacity loss.
Follows the methodology:
- Scenario A (No Action): Late reaction → capacity loss → emergency fuel costs
- Scenario B (With Action): Prevention → less capacity loss → lower costs

Returns RELATIVE avoided costs, not absolute exact costs (standard in energy planning).
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from src.db.models import PowerPlant


@dataclass
class EconomicScenarioResult:
    """Result for a single economic scenario (no_action or with_action)."""

    capacity_loss_pct: float
    capacity_lost_mw: float
    lost_generation_mwh: float
    replacement_cost_usd: float
    emergency_fuel_cost_usd: float
    total_cost_usd: float


@dataclass
class EconomicDelta:
    """Comparison between no_action and with_action scenarios."""

    no_action: EconomicScenarioResult
    with_action: EconomicScenarioResult
    savings_usd: float
    savings_pct: float
    summary: str


class EconomicCostCalculator:
    """Calculates avoided costs from water stress mitigation on power plants.

    The core calculation:
    1. SPI determines capacity loss percentage
    2. Capacity loss × hours × prices = cost
    3. Compare: cost_no_action - cost_with_action = savings
    """

    # Capacity loss rules based on SPI thresholds
    # These are relative impact factors, not absolute values
    CAPACITY_LOSS_RULES = [
        # (spi_min, spi_max, capacity_loss_pct)
        (-0.5, float("inf"), 0.00),   # Normal conditions - no loss
        (-1.0, -0.5, 0.05),            # Mild drought - 5% capacity loss
        (-1.5, -1.0, 0.15),            # Moderate drought - 15% capacity loss
        (-2.0, -1.5, 0.30),            # Severe drought - 30% capacity loss
        (float("-inf"), -2.0, 0.50),  # Extreme drought - 50% capacity loss
    ]

    # Water dependency multipliers
    WATER_DEPENDENCY_FACTOR = {
        "high": 1.0,      # Full impact from water stress
        "medium": 0.6,    # 60% of baseline impact
        "low": 0.3,       # 30% of baseline impact
    }

    # Cooling type multipliers
    COOLING_TYPE_FACTOR = {
        "once_through": 1.2,    # Most water-dependent, higher impact
        "recirculating": 1.0,   # Standard impact
        "dry": 0.2,             # Minimal water dependency
    }

    # Heat rate for fuel cost calculation (MMBtu per MWh)
    # Average for natural gas combined cycle plants
    DEFAULT_HEAT_RATE = 7.0

    def __init__(self, heat_rate: float = None):
        """Initialize calculator.

        Args:
            heat_rate: MMBtu of fuel per MWh generated. Default 7.0 for gas plants.
        """
        self.heat_rate = heat_rate or self.DEFAULT_HEAT_RATE

    def calculate_capacity_loss_pct(
        self,
        spi: float,
        water_dependency: str = "high",
        cooling_type: str = "recirculating",
    ) -> float:
        """Calculate percentage of plant capacity lost due to water stress.

        Args:
            spi: Current SPI-6 value
            water_dependency: Plant's water dependency level
            cooling_type: Type of cooling system

        Returns:
            Capacity loss as decimal (0.0 to 1.0)
        """
        # Find base capacity loss from SPI
        base_loss = 0.0
        for spi_min, spi_max, loss_pct in self.CAPACITY_LOSS_RULES:
            if spi_min < spi <= spi_max:
                base_loss = loss_pct
                break

        # Apply plant-specific factors
        dep_factor = self.WATER_DEPENDENCY_FACTOR.get(water_dependency, 1.0)
        cool_factor = self.COOLING_TYPE_FACTOR.get(cooling_type, 1.0)

        adjusted_loss = base_loss * dep_factor * cool_factor

        # Cap at 80% max capacity loss
        return min(adjusted_loss, 0.80)

    def calculate_emergency_fuel_cost(
        self,
        capacity_lost_mw: float,
        hours: int,
        fuel_price_usd_mmbtu: float,
    ) -> float:
        """Calculate cost of emergency fuel purchases to replace lost capacity.

        When a plant loses capacity due to water stress, grid operators must:
        1. Purchase replacement power (captured in replacement_cost)
        2. OR run peaker plants on emergency fuel (captured here)

        Formula: cost = capacity_lost_mw × hours × heat_rate × fuel_price

        Args:
            capacity_lost_mw: MW of capacity unavailable
            hours: Number of hours of lost capacity
            fuel_price_usd_mmbtu: Natural gas price in USD per MMBtu

        Returns:
            Emergency fuel cost in USD
        """
        # Energy that needs replacement
        energy_mwh = capacity_lost_mw * hours

        # Fuel needed (MMBtu)
        fuel_mmbtu = energy_mwh * self.heat_rate

        # Cost
        return fuel_mmbtu * fuel_price_usd_mmbtu

    def calculate_replacement_cost(
        self,
        capacity_lost_mw: float,
        hours: int,
        marginal_price_usd_mwh: float,
    ) -> float:
        """Calculate cost of purchasing replacement power on the market.

        When a plant can't generate, power must be bought at marginal prices.

        Args:
            capacity_lost_mw: MW of capacity unavailable
            hours: Number of hours of lost capacity
            marginal_price_usd_mwh: Market price for electricity

        Returns:
            Replacement power cost in USD
        """
        energy_mwh = capacity_lost_mw * hours
        return energy_mwh * marginal_price_usd_mwh

    def calculate_scenario_cost(
        self,
        plant: PowerPlant,
        spi: float,
        projection_days: int,
        marginal_price_usd_mwh: float,
        fuel_price_usd_mmbtu: float,
    ) -> EconomicScenarioResult:
        """Calculate economic cost for a single scenario.

        Args:
            plant: PowerPlant model instance
            spi: SPI value for this scenario
            projection_days: Number of days to project
            marginal_price_usd_mwh: Electricity market price
            fuel_price_usd_mmbtu: Natural gas price

        Returns:
            EconomicScenarioResult with all cost components
        """
        # Calculate capacity loss
        capacity_loss_pct = self.calculate_capacity_loss_pct(
            spi=spi,
            water_dependency=plant.water_dependency,
            cooling_type=plant.cooling_type,
        )

        capacity_lost_mw = plant.capacity_mw * capacity_loss_pct

        # Convert days to hours (assume 24h operation)
        hours = projection_days * 24

        # Calculate lost generation
        lost_generation_mwh = capacity_lost_mw * hours

        # Calculate costs
        replacement_cost = self.calculate_replacement_cost(
            capacity_lost_mw=capacity_lost_mw,
            hours=hours,
            marginal_price_usd_mwh=marginal_price_usd_mwh,
        )

        emergency_fuel_cost = self.calculate_emergency_fuel_cost(
            capacity_lost_mw=capacity_lost_mw,
            hours=hours,
            fuel_price_usd_mmbtu=fuel_price_usd_mmbtu,
        )

        # Total cost is the higher of replacement or emergency fuel
        # (operators choose the cheaper option, but we estimate based on replacement)
        total_cost = replacement_cost

        return EconomicScenarioResult(
            capacity_loss_pct=capacity_loss_pct,
            capacity_lost_mw=capacity_lost_mw,
            lost_generation_mwh=lost_generation_mwh,
            replacement_cost_usd=replacement_cost,
            emergency_fuel_cost_usd=emergency_fuel_cost,
            total_cost_usd=total_cost,
        )

    def calculate_economic_delta(
        self,
        plant: PowerPlant,
        spi_no_action: float,
        spi_with_action: float,
        projection_days: int,
        marginal_price_usd_mwh: float,
        fuel_price_usd_mmbtu: float,
    ) -> EconomicDelta:
        """Compare costs between no-action and with-action scenarios.

        This is the main calculation that shows savings from prevention.

        Args:
            plant: PowerPlant to analyze
            spi_no_action: Projected SPI without intervention
            spi_with_action: Projected SPI with water actions
            projection_days: Days to project forward
            marginal_price_usd_mwh: Electricity price
            fuel_price_usd_mmbtu: Fuel price

        Returns:
            EconomicDelta with comparison and savings
        """
        no_action = self.calculate_scenario_cost(
            plant=plant,
            spi=spi_no_action,
            projection_days=projection_days,
            marginal_price_usd_mwh=marginal_price_usd_mwh,
            fuel_price_usd_mmbtu=fuel_price_usd_mmbtu,
        )

        with_action = self.calculate_scenario_cost(
            plant=plant,
            spi=spi_with_action,
            projection_days=projection_days,
            marginal_price_usd_mwh=marginal_price_usd_mwh,
            fuel_price_usd_mmbtu=fuel_price_usd_mmbtu,
        )

        savings_usd = no_action.total_cost_usd - with_action.total_cost_usd
        savings_pct = (
            (savings_usd / no_action.total_cost_usd * 100)
            if no_action.total_cost_usd > 0
            else 0.0
        )

        # Generate summary
        summary = self._generate_summary(plant, no_action, with_action, savings_usd)

        return EconomicDelta(
            no_action=no_action,
            with_action=with_action,
            savings_usd=savings_usd,
            savings_pct=savings_pct,
            summary=summary,
        )

    def _generate_summary(
        self,
        plant: PowerPlant,
        no_action: EconomicScenarioResult,
        with_action: EconomicScenarioResult,
        savings_usd: float,
    ) -> str:
        """Generate human-readable summary of economic analysis."""
        if savings_usd <= 0:
            return (
                f"No economic benefit from intervention for {plant.name}. "
                f"Water stress does not significantly impact this plant's capacity."
            )

        capacity_diff = no_action.capacity_loss_pct - with_action.capacity_loss_pct

        return (
            f"Implementing water actions for {plant.name} ({plant.capacity_mw:.0f} MW) "
            f"reduces capacity loss from {no_action.capacity_loss_pct:.0%} to "
            f"{with_action.capacity_loss_pct:.0%}, "
            f"avoiding ${savings_usd:,.0f} in emergency fuel and replacement costs."
        )

    def calculate_daily_costs(
        self,
        plant: PowerPlant,
        spi_trajectory_no_action: list[dict],
        spi_trajectory_with_action: list[dict],
        marginal_price_usd_mwh: float,
    ) -> dict:
        """Calculate economic impact day-by-day for more accurate savings.
        
        This method captures savings from days where actions keep conditions
        in a better SPI bucket (e.g., 30% loss instead of 50% loss).
        
        Args:
            plant: PowerPlant to analyze
            spi_trajectory_no_action: List of {day, projected_spi} for no-action
            spi_trajectory_with_action: List of {day, projected_spi} for with-action
            marginal_price_usd_mwh: Electricity price
            
        Returns:
            Dict with daily costs and totals
        """
        total_no_action = 0.0
        total_with_action = 0.0
        
        hours_per_day = 24
        
        for i, day_no_action in enumerate(spi_trajectory_no_action):
            spi_no = day_no_action.get("projected_spi", -1.5)
            
            # Get corresponding with-action SPI (or use same day index)
            if i < len(spi_trajectory_with_action):
                spi_with = spi_trajectory_with_action[i].get("projected_spi", spi_no)
            else:
                spi_with = spi_no + 0.3  # Default improvement if trajectory shorter
            
            # Calculate capacity loss for each scenario
            loss_no = self.calculate_capacity_loss_pct(
                spi=spi_no,
                water_dependency=plant.water_dependency,
                cooling_type=plant.cooling_type,
            )
            loss_with = self.calculate_capacity_loss_pct(
                spi=spi_with,
                water_dependency=plant.water_dependency,
                cooling_type=plant.cooling_type,
            )
            
            # Daily costs
            daily_cost_no = plant.capacity_mw * loss_no * hours_per_day * marginal_price_usd_mwh
            daily_cost_with = plant.capacity_mw * loss_with * hours_per_day * marginal_price_usd_mwh
            
            total_no_action += daily_cost_no
            total_with_action += daily_cost_with
        
        return {
            "total_no_action": total_no_action,
            "total_with_action": total_with_action,
            "savings": total_no_action - total_with_action,
            "days": len(spi_trajectory_no_action),
        }

    def aggregate_plants(
        self,
        plants: list[PowerPlant],
        spi_no_action: float,
        spi_with_action: float,
        projection_days: int,
        marginal_price_usd_mwh: float,
        fuel_price_usd_mmbtu: float,
        spi_trajectory_no_action: list[dict] = None,
        spi_trajectory_with_action: list[dict] = None,
    ) -> dict:
        """Calculate aggregate economic impact across multiple plants.

        Args:
            plants: List of PowerPlant instances
            spi_no_action: Projected SPI without intervention (used if no trajectory)
            spi_with_action: Projected SPI with water actions (used if no trajectory)
            projection_days: Days to project
            marginal_price_usd_mwh: Electricity price
            fuel_price_usd_mmbtu: Fuel price
            spi_trajectory_no_action: Optional daily SPI trajectory without action
            spi_trajectory_with_action: Optional daily SPI trajectory with action

        Returns:
            Dict with aggregated results and per-plant breakdown
        """
        per_plant_results = []
        total_no_action = 0.0
        total_with_action = 0.0
        total_savings = 0.0
        
        # Use day-by-day calculation if trajectories are provided
        use_daily_calc = (
            spi_trajectory_no_action is not None 
            and spi_trajectory_with_action is not None
            and len(spi_trajectory_no_action) > 0
        )

        for plant in plants:
            if use_daily_calc:
                # Day-by-day calculation captures savings from days where
                # actions keep conditions in a better SPI bucket
                daily_result = self.calculate_daily_costs(
                    plant=plant,
                    spi_trajectory_no_action=spi_trajectory_no_action,
                    spi_trajectory_with_action=spi_trajectory_with_action,
                    marginal_price_usd_mwh=marginal_price_usd_mwh,
                )
                
                # Calculate effective capacity loss from actual costs
                # This reflects the day-by-day calculation accurately
                hours = len(spi_trajectory_no_action) * 24
                max_possible_cost = plant.capacity_mw * hours * marginal_price_usd_mwh
                
                effective_loss_no = (
                    daily_result["total_no_action"] / max_possible_cost
                    if max_possible_cost > 0
                    else 0
                )
                effective_loss_with = (
                    daily_result["total_with_action"] / max_possible_cost
                    if max_possible_cost > 0
                    else 0
                )
                
                per_plant_results.append({
                    "plant_id": str(plant.id),
                    "plant_name": plant.name,
                    "capacity_mw": plant.capacity_mw,
                    "no_action_cost_usd": daily_result["total_no_action"],
                    "with_action_cost_usd": daily_result["total_with_action"],
                    "savings_usd": daily_result["savings"],
                    "capacity_loss_no_action": effective_loss_no,
                    "capacity_loss_with_action": effective_loss_with,
                })
                
                total_no_action += daily_result["total_no_action"]
                total_with_action += daily_result["total_with_action"]
                total_savings += daily_result["savings"]
            else:
                # Fallback to single-point calculation
                delta = self.calculate_economic_delta(
                    plant=plant,
                    spi_no_action=spi_no_action,
                    spi_with_action=spi_with_action,
                    projection_days=projection_days,
                    marginal_price_usd_mwh=marginal_price_usd_mwh,
                    fuel_price_usd_mmbtu=fuel_price_usd_mmbtu,
                )

                per_plant_results.append({
                    "plant_id": str(plant.id),
                    "plant_name": plant.name,
                    "capacity_mw": plant.capacity_mw,
                    "no_action_cost_usd": delta.no_action.total_cost_usd,
                    "with_action_cost_usd": delta.with_action.total_cost_usd,
                    "savings_usd": delta.savings_usd,
                    "capacity_loss_no_action": delta.no_action.capacity_loss_pct,
                    "capacity_loss_with_action": delta.with_action.capacity_loss_pct,
                })

                total_no_action += delta.no_action.total_cost_usd
                total_with_action += delta.with_action.total_cost_usd
                total_savings += delta.savings_usd

        total_capacity = sum(p.capacity_mw for p in plants)
        savings_pct = (
            (total_savings / total_no_action * 100)
            if total_no_action > 0
            else 0.0
        )

        return {
            "plants_analyzed": len(plants),
            "total_capacity_mw": total_capacity,
            "total_cost_no_action_usd": total_no_action,
            "total_cost_with_action_usd": total_with_action,
            "total_savings_usd": total_savings,
            "savings_pct": savings_pct,
            "per_plant_breakdown": per_plant_results,
            "calculated_at": datetime.utcnow().isoformat(),
        }
