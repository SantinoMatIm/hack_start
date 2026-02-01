"""Heuristic registry for coordinating all heuristic rules.

Updated to use the 15 new heuristics based on the technical document.
"""

from typing import Optional
from sqlalchemy.orm import Session

from src.config.constants import RiskLevel, Trend, Profile
from src.db.models import Zone, Action
from src.heuristics.base_heuristic import BaseHeuristic, HeuristicContext, HeuristicResult

# New heuristics based on technical document
from src.heuristics.h1_persistence_trigger import H1PersistenceTrigger
from src.heuristics.h2_flash_drought import H2FlashDrought
from src.heuristics.h3_seasonality_check import H3SeasonalityCheck
from src.heuristics.h4_phenological_stress import H4PhenologicalStress
from src.heuristics.h5_trend_prediction import H5TrendPrediction
from src.heuristics.h6_wet_season_failure import H6WetSeasonFailure
from src.heuristics.h7_reservoir_lag import H7ReservoirLag
from src.heuristics.h8_groundwater_proxy import H8GroundwaterProxy
from src.heuristics.h9_scale_differential import H9ScaleDifferential
from src.heuristics.h10_drought_magnitude import H10DroughtMagnitude
from src.heuristics.h11_markov_transition import H11MarkovTransition
from src.heuristics.h12_weather_whiplash import H12WeatherWhiplash
from src.heuristics.h13_cooling_towers import H13CoolingTowers
from src.heuristics.h14_infrastructure_defense import H14InfrastructureDefense
from src.heuristics.h15_stepdown_recovery import H15StepdownRecovery


class HeuristicRegistry:
    """
    Registry for all heuristic rules.

    Coordinates evaluation of all heuristics and aggregates results.

    The 15 heuristics are organized into 4 blocks:
    - Block I (H1-H3): Early Detection and Rapid Dynamics
    - Block II (H4-H6): Agricultural Impact and Seasonal Trends
    - Block III (H7-H9): Hydrological Security and Infrastructure
    - Block IV (H10-H15): Operational Response and Demand Management
    """

    def __init__(self, session: Optional[Session] = None):
        self.session = session
        self._heuristics: list[BaseHeuristic] = [
            # Block I: Early Detection
            H1PersistenceTrigger(),
            H2FlashDrought(),
            H3SeasonalityCheck(),
            # Block II: Agricultural Impact
            H4PhenologicalStress(),
            H5TrendPrediction(),
            H6WetSeasonFailure(),
            # Block III: Hydrological Security
            H7ReservoirLag(),
            H8GroundwaterProxy(),
            H9ScaleDifferential(),
            # Block IV: Operational Response
            H10DroughtMagnitude(),
            H11MarkovTransition(),
            H12WeatherWhiplash(),
            H13CoolingTowers(),
            H14InfrastructureDefense(),
            H15StepdownRecovery(),
        ]

    def get_heuristic(self, heuristic_id: str) -> Optional[BaseHeuristic]:
        """Get a specific heuristic by ID."""
        for h in self._heuristics:
            if h.heuristic_id == heuristic_id:
                return h
        return None

    def evaluate_all(self, context: HeuristicContext) -> list[HeuristicResult]:
        """
        Evaluate all heuristics and return activated ones.

        Args:
            context: Current risk context

        Returns:
            List of HeuristicResults for activated heuristics
        """
        results = []

        for heuristic in self._heuristics:
            result = heuristic.evaluate(context)
            if result.activated:
                results.append(result)

        # Sort by priority (highest first)
        results.sort(key=lambda r: r.priority_score, reverse=True)

        return results

    def build_context(
        self,
        spi: float = None,
        spi_1: float = None,
        spi_3: float = None,
        spi_6: float = None,
        spi_12: float = None,
        spi_24: float = None,
        spi_48: float = None,
        risk_level: RiskLevel = RiskLevel.LOW,
        trend: Trend = Trend.STABLE,
        days_to_critical: Optional[int] = None,
        profile: Profile = Profile.GOVERNMENT,
        zone_slug: str = "",
        rapid_deterioration: bool = False,
        recent_spi_change: Optional[float] = None,
        # New fields for advanced heuristics
        consecutive_dry_periods: int = 0,
        current_spi_category: Optional[int] = None,
        spi_category_4_weeks_ago: Optional[int] = None,
        is_dry_season: bool = False,
        absolute_precipitation_deficit_mm: Optional[float] = None,
        is_critical_phenological_window: bool = False,
        crops_affected: list[str] = None,
        phenological_stages: list[str] = None,
        sen_slope_per_month: Optional[float] = None,
        mann_kendall_confidence: Optional[float] = None,
        mann_kendall_trend: Optional[str] = None,
        wet_season_average_spi: Optional[float] = None,
        wet_season_locked: bool = False,
        reservoir_storage_pct: Optional[float] = None,
        scale_differential: Optional[float] = None,
        drought_magnitude: Optional[float] = None,
        magnitude_percentile: Optional[float] = None,
        drought_duration_months: int = 0,
        transition_prob_to_severe: Optional[float] = None,
        markov_current_state: Optional[str] = None,
        recent_wet_to_dry_transition: bool = False,
        months_since_wet_period: Optional[int] = None,
        industrial_coc_current: Optional[float] = None,
        demand_capacity_ratio: Optional[float] = None,
        all_scales_positive_months: int = 0,
    ) -> HeuristicContext:
        """
        Build a HeuristicContext from individual parameters.

        Supports both legacy (spi) and new (spi_6) field names.
        """
        # Handle legacy 'spi' parameter
        effective_spi_6 = spi_6 if spi_6 is not None else spi

        return HeuristicContext(
            # Core context
            risk_level=risk_level,
            trend=trend,
            days_to_critical=days_to_critical,
            profile=profile,
            zone_slug=zone_slug,
            rapid_deterioration=rapid_deterioration,
            recent_spi_change=recent_spi_change,
            # Multi-scale SPI
            spi_1=spi_1,
            spi_3=spi_3,
            spi_6=effective_spi_6,
            spi_12=spi_12,
            spi_24=spi_24,
            spi_48=spi_48,
            # H1: Persistence
            consecutive_dry_periods=consecutive_dry_periods,
            # H2: Flash drought
            current_spi_category=current_spi_category,
            spi_category_4_weeks_ago=spi_category_4_weeks_ago,
            # H3: Seasonality
            is_dry_season=is_dry_season,
            absolute_precipitation_deficit_mm=absolute_precipitation_deficit_mm,
            # H4: Phenology
            is_critical_phenological_window=is_critical_phenological_window,
            crops_affected=crops_affected or [],
            phenological_stages=phenological_stages or [],
            # H5: Statistical trend
            sen_slope_per_month=sen_slope_per_month,
            mann_kendall_confidence=mann_kendall_confidence,
            mann_kendall_trend=mann_kendall_trend,
            # H6: Wet season
            wet_season_average_spi=wet_season_average_spi,
            wet_season_locked=wet_season_locked,
            # H7: Reservoir
            reservoir_storage_pct=reservoir_storage_pct,
            # H9: Scale differential
            scale_differential=scale_differential,
            # H10: Magnitude
            drought_magnitude=drought_magnitude,
            magnitude_percentile=magnitude_percentile,
            drought_duration_months=drought_duration_months,
            # H11: Markov
            transition_prob_to_severe=transition_prob_to_severe,
            markov_current_state=markov_current_state,
            # H12: Weather whiplash
            recent_wet_to_dry_transition=recent_wet_to_dry_transition,
            months_since_wet_period=months_since_wet_period,
            # H13: Industrial
            industrial_coc_current=industrial_coc_current,
            # H14: Infrastructure
            demand_capacity_ratio=demand_capacity_ratio,
            # H15: Recovery
            all_scales_positive_months=all_scales_positive_months,
        )

    def get_applicable_actions(
        self,
        results: list[HeuristicResult],
    ) -> list[str]:
        """
        Get all unique action codes from activated heuristics.

        Args:
            results: List of activated heuristic results

        Returns:
            List of unique action codes
        """
        action_codes = set()
        for result in results:
            action_codes.update(result.applicable_actions)
        return list(action_codes)

    def get_actions_from_db(
        self,
        action_codes: list[str],
    ) -> list[Action]:
        """
        Fetch action details from database.

        Args:
            action_codes: List of action codes to fetch

        Returns:
            List of Action model instances
        """
        if not self.session or not action_codes:
            return []

        return (
            self.session.query(Action)
            .filter(Action.code.in_(action_codes))
            .all()
        )

    def get_recommended_actions(
        self,
        context: HeuristicContext,
    ) -> dict:
        """
        Get recommended actions for a given context.

        Evaluates all heuristics, collects applicable actions,
        and returns prioritized recommendations.

        Args:
            context: Current risk context

        Returns:
            Dictionary with activated heuristics and recommended actions
        """
        # Evaluate all heuristics
        results = self.evaluate_all(context)

        # Get unique action codes
        action_codes = self.get_applicable_actions(results)

        # Fetch action details if session available
        actions = self.get_actions_from_db(action_codes)
        actions_by_code = {a.code: a for a in actions}

        # Build recommendations
        recommendations = []

        for result in results:
            for action_code in result.applicable_actions:
                action = actions_by_code.get(action_code)

                recommendation = {
                    "action_code": action_code,
                    "heuristic_id": result.heuristic_id,
                    "priority_score": result.priority_score,
                    "justification": result.justification,
                    "default_parameters": result.parameters,
                }

                if action:
                    recommendation.update({
                        "title": action.title,
                        "description": action.description,
                        "impact_formula": action.impact_formula,
                        "default_urgency_days": action.default_urgency_days,
                        "parameter_schema": action.parameter_schema,
                    })

                recommendations.append(recommendation)

        # Sort by priority
        recommendations.sort(key=lambda r: r["priority_score"], reverse=True)

        # Build context summary for response
        context_summary = {
            "spi_1": context.spi_1,
            "spi_3": context.spi_3,
            "spi_6": context.spi_6,
            "spi_12": context.spi_12,
            "spi_24": context.spi_24,
            "spi_48": context.spi_48,
            "risk_level": context.risk_level.value,
            "trend": context.trend.value,
            "days_to_critical": context.days_to_critical,
            "profile": context.profile.value,
            "zone": context.zone_slug,
        }

        return {
            "context": context_summary,
            "activated_heuristics": [
                {
                    "id": r.heuristic_id,
                    "priority": r.priority_score,
                    "actions_count": len(r.applicable_actions),
                }
                for r in results
            ],
            "recommendations": recommendations,
        }
