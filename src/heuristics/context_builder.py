"""Context builder for populating HeuristicContext with all required data.

Orchestrates all analysis components to build a complete context for
heuristic evaluation.
"""

from datetime import date
from typing import Optional
import numpy as np
import pandas as pd

from src.heuristics.base_heuristic import HeuristicContext
from src.config.constants import RiskLevel, Trend, Profile, classify_risk_level
from src.risk_engine.multi_scale_spi import MultiScaleSPICalculator
from src.risk_engine.trend_analyzer import TrendAnalyzer
from src.risk_engine.critical_estimator import CriticalEstimator
from src.risk_engine.statistical_trend_analyzer import StatisticalTrendAnalyzer
from src.risk_engine.drought_magnitude import DroughtMagnitudeCalculator
from src.risk_engine.markov_analyzer import MarkovTransitionAnalyzer
from src.risk_engine.seasonality_detector import SeasonalityDetector
from src.risk_engine.phenology_calendar import PhenologyCalendar


class HeuristicContextBuilder:
    """
    Builds complete HeuristicContext for heuristic evaluation.

    Orchestrates all analysis components:
    - MultiScaleSPICalculator: SPI at 1, 3, 6, 12, 24, 48 months
    - StatisticalTrendAnalyzer: Mann-Kendall test and Sen slope
    - MarkovTransitionAnalyzer: State transition probabilities
    - SeasonalityDetector: Dry/wet season classification
    - PhenologyCalendar: Critical crop growth windows
    - DroughtMagnitudeCalculator: Cumulative severity
    """

    def __init__(
        self,
        zone_slug: str,
        profile: Profile = Profile.GOVERNMENT,
        crops: list[str] = None
    ):
        """
        Initialize builder for a specific zone.

        Args:
            zone_slug: Zone identifier
            profile: User profile (government/industry)
            crops: List of crops to monitor for phenology
        """
        self.zone_slug = zone_slug
        self.profile = profile

        # Initialize analysis components
        self.multi_spi = MultiScaleSPICalculator()
        self.trend_analyzer = TrendAnalyzer()
        self.critical_estimator = CriticalEstimator()
        self.stat_trend = StatisticalTrendAnalyzer()
        self.magnitude_calc = DroughtMagnitudeCalculator()
        self.markov = MarkovTransitionAnalyzer()
        self.seasonality = SeasonalityDetector(zone_slug)
        self.phenology = PhenologyCalendar(crops or ["maiz", "frijol"])

    def build_context(
        self,
        daily_precip: pd.DataFrame,
        reservoir_storage_pct: Optional[float] = None,
        demand_capacity_ratio: Optional[float] = None,
        industrial_coc: Optional[float] = None,
        ref_date: Optional[date] = None
    ) -> HeuristicContext:
        """
        Build complete HeuristicContext from precipitation data.

        Args:
            daily_precip: DataFrame with 'date' and 'precipitation_mm' columns
            reservoir_storage_pct: Optional reservoir storage percentage
            demand_capacity_ratio: Optional demand/capacity ratio
            industrial_coc: Optional current Cycles of Concentration
            ref_date: Reference date (default: today)

        Returns:
            Fully populated HeuristicContext
        """
        ref_date = ref_date or date.today()

        # 1. Calculate multi-scale SPI
        multi_spi = self.multi_spi.get_current_multi_spi(daily_precip)
        spi_6 = multi_spi.get("spi_6") or 0.0

        # 2. Get SPI series for trend analysis
        all_spi = self.multi_spi.calculate_all_scales(daily_precip)
        spi_6_series = all_spi.get(6, pd.DataFrame())
        spi_3_series = all_spi.get(3, pd.DataFrame())

        # 3. Basic trend and risk classification
        trend_result = self._analyze_trend(spi_6_series)
        risk_level = classify_risk_level(spi_6)
        days_to_critical = self._estimate_days_critical(spi_6, trend_result, spi_6_series)

        # 4. Statistical trend analysis (H5)
        stat_result = self._analyze_statistical_trend(spi_6_series)

        # 5. Markov analysis (H11)
        markov_result = self._analyze_markov(spi_6, spi_6_series)

        # 6. Drought magnitude (H10)
        magnitude_result = self._analyze_magnitude(spi_6_series)

        # 7. Seasonality (H3, H6)
        season_result = self._analyze_seasonality(spi_6_series, ref_date)

        # 8. Phenology (H4)
        pheno_result = self.phenology.get_phenological_context(ref_date)

        # 9. Flash drought detection (H2)
        flash_result = self._detect_flash_drought(spi_6_series)

        # 10. Persistence (H1)
        persistence_result = self._analyze_persistence(spi_3_series)

        # 11. Scale differential (H9)
        scale_diff = self._calculate_scale_differential(multi_spi)

        # 12. Weather whiplash (H12)
        whiplash_result = self._detect_weather_whiplash(spi_6_series)

        # 13. Recovery tracking (H15)
        recovery_months = self.multi_spi.count_consecutive_positive_months(daily_precip)

        return HeuristicContext(
            # Core context
            risk_level=risk_level,
            trend=trend_result["trend"],
            days_to_critical=days_to_critical,
            profile=self.profile,
            zone_slug=self.zone_slug,
            rapid_deterioration=trend_result.get("rapid_deterioration", False),

            # Multi-scale SPI
            spi_1=multi_spi.get("spi_1"),
            spi_3=multi_spi.get("spi_3"),
            spi_6=multi_spi.get("spi_6"),
            spi_12=multi_spi.get("spi_12"),
            spi_24=multi_spi.get("spi_24"),
            spi_48=multi_spi.get("spi_48"),

            # H1: Persistence
            consecutive_dry_periods=persistence_result["consecutive_dry_periods"],
            spi_3_previous_period=persistence_result.get("previous_spi_3"),

            # H2: Flash drought
            current_spi_category=flash_result["current_category"],
            spi_category_4_weeks_ago=flash_result["category_4_weeks_ago"],

            # H3: Seasonality
            is_dry_season=season_result["is_dry_season"],
            absolute_precipitation_deficit_mm=season_result.get("deficit_mm"),

            # H4: Phenology
            is_critical_phenological_window=pheno_result["is_critical_phenological_window"],
            crops_affected=pheno_result["crops_affected"],
            phenological_stages=pheno_result["phenological_stages"],
            phenological_severity_multiplier=pheno_result["severity_multiplier"],

            # H5: Statistical trend
            sen_slope_per_month=stat_result["slope"],
            mann_kendall_confidence=stat_result["confidence"],
            mann_kendall_trend=stat_result["trend"],

            # H6: Wet season
            wet_season_average_spi=season_result.get("wet_season_avg_spi"),
            wet_season_locked=season_result.get("wet_season_locked", False),

            # H7: Reservoir
            reservoir_storage_pct=reservoir_storage_pct,

            # H9: Scale differential
            scale_differential=scale_diff,
            false_recovery_detected=self._is_false_recovery(multi_spi),

            # H10: Magnitude
            drought_magnitude=magnitude_result["magnitude"],
            magnitude_percentile=magnitude_result["percentile"],
            drought_duration_months=magnitude_result["duration"],
            drought_min_spi=magnitude_result.get("min_spi"),
            severity_tier=magnitude_result.get("tier"),

            # H11: Markov
            transition_prob_to_severe=markov_result["prob_severe"],
            transition_prob_to_extreme=markov_result.get("prob_extreme"),
            markov_current_state=markov_result["state"],

            # H12: Weather whiplash
            recent_wet_to_dry_transition=whiplash_result["detected"],
            months_since_wet_period=whiplash_result.get("months_since_wet"),

            # H13: Industrial
            industrial_coc_current=industrial_coc,

            # H14: Infrastructure
            demand_capacity_ratio=demand_capacity_ratio,

            # H15: Recovery
            all_scales_positive_months=recovery_months,
        )

    def _analyze_trend(self, spi_series: pd.DataFrame) -> dict:
        """Analyze basic trend from SPI series."""
        if spi_series.empty or len(spi_series) < 2:
            return {"trend": Trend.STABLE, "rapid_deterioration": False}

        try:
            result = self.trend_analyzer.get_trend_summary(spi_series)
            return {
                "trend": result.get("trend", Trend.STABLE),
                "rapid_deterioration": result.get("rapid_deterioration", False),
            }
        except Exception:
            return {"trend": Trend.STABLE, "rapid_deterioration": False}

    def _estimate_days_critical(
        self,
        current_spi: float,
        trend_result: dict,
        spi_series: pd.DataFrame
    ) -> Optional[int]:
        """Estimate days until critical threshold."""
        try:
            return self.critical_estimator.estimate_days_to_critical(
                current_spi,
                trend_result.get("trend", Trend.STABLE),
                spi_series
            )
        except Exception:
            return None

    def _analyze_statistical_trend(self, spi_series: pd.DataFrame) -> dict:
        """Perform Mann-Kendall and Sen slope analysis."""
        if spi_series.empty or len(spi_series) < 6:
            return {"slope": None, "confidence": None, "trend": None}

        try:
            values = spi_series["spi"].values
            result = self.stat_trend.analyze_trend(values)
            return {
                "slope": result["slope_per_month"],
                "confidence": result["confidence_pct"],
                "trend": result["trend_direction"],
            }
        except Exception:
            return {"slope": None, "confidence": None, "trend": None}

    def _analyze_markov(
        self,
        current_spi: float,
        spi_series: pd.DataFrame
    ) -> dict:
        """Analyze Markov transition probabilities."""
        if spi_series.empty or len(spi_series) < 12:
            return {"state": None, "prob_severe": None, "prob_extreme": None}

        try:
            result = self.markov.analyze_current_position(current_spi, spi_series)
            return {
                "state": result["current_state"],
                "prob_severe": result["transition_prob_to_severe"],
                "prob_extreme": result["transition_prob_to_extreme"],
            }
        except Exception:
            return {"state": None, "prob_severe": None, "prob_extreme": None}

    def _analyze_magnitude(self, spi_series: pd.DataFrame) -> dict:
        """Calculate drought magnitude and percentile."""
        if spi_series.empty:
            return {
                "magnitude": None,
                "percentile": None,
                "duration": 0,
                "min_spi": None,
                "tier": None,
            }

        try:
            self.magnitude_calc.fit_historical(spi_series)
            result = self.magnitude_calc.get_magnitude_context(spi_series)
            return {
                "magnitude": result["drought_magnitude"],
                "percentile": result["magnitude_percentile"],
                "duration": result["drought_duration_months"],
                "min_spi": result.get("drought_min_spi"),
                "tier": result.get("severity_tier"),
            }
        except Exception:
            return {
                "magnitude": None,
                "percentile": None,
                "duration": 0,
                "min_spi": None,
                "tier": None,
            }

    def _analyze_seasonality(
        self,
        spi_series: pd.DataFrame,
        ref_date: date
    ) -> dict:
        """Analyze seasonal context."""
        is_dry = self.seasonality.is_dry_season(ref_date)
        wet_avg = None
        locked = False

        if not spi_series.empty and "month" in spi_series.columns:
            wet_avg = self.seasonality.get_wet_season_spi_average(spi_series)
            locked = wet_avg is not None and wet_avg < -1.0

        return {
            "is_dry_season": is_dry,
            "wet_season_avg_spi": wet_avg,
            "wet_season_locked": locked,
            "deficit_mm": None,
        }

    def _detect_flash_drought(self, spi_series: pd.DataFrame) -> dict:
        """Detect flash drought conditions."""
        if spi_series.empty or len(spi_series) < 2:
            return {"current_category": None, "category_4_weeks_ago": None}

        try:
            current = spi_series.iloc[-1]["spi"]
            prev = spi_series.iloc[-2]["spi"] if len(spi_series) >= 2 else current

            return {
                "current_category": self.markov.spi_to_category(current),
                "category_4_weeks_ago": self.markov.spi_to_category(prev),
            }
        except Exception:
            return {"current_category": None, "category_4_weeks_ago": None}

    def _analyze_persistence(self, spi_3_series: pd.DataFrame) -> dict:
        """Analyze drought persistence for H1."""
        if spi_3_series.empty:
            return {"consecutive_dry_periods": 0, "previous_spi_3": None}

        try:
            count = 0
            for val in reversed(spi_3_series["spi"].values):
                if val < -1.0:
                    count += 1
                else:
                    break

            prev_spi = (
                float(spi_3_series.iloc[-2]["spi"])
                if len(spi_3_series) >= 2 else None
            )

            return {
                "consecutive_dry_periods": count,
                "previous_spi_3": prev_spi,
            }
        except Exception:
            return {"consecutive_dry_periods": 0, "previous_spi_3": None}

    def _calculate_scale_differential(self, multi_spi: dict) -> Optional[float]:
        """Calculate differential between short and long-term SPI."""
        spi_1 = multi_spi.get("spi_1")
        spi_12 = multi_spi.get("spi_12")

        if spi_1 is None or spi_12 is None:
            return None

        return abs(spi_1 - spi_12)

    def _is_false_recovery(self, multi_spi: dict) -> bool:
        """Detect false recovery (green drought)."""
        spi_1 = multi_spi.get("spi_1")
        spi_12 = multi_spi.get("spi_12")

        if spi_1 is None or spi_12 is None:
            return False

        return (
            abs(spi_1 - spi_12) > 1.5 and
            spi_12 < -1.0 and
            spi_1 > spi_12
        )

    def _detect_weather_whiplash(self, spi_series: pd.DataFrame) -> dict:
        """Detect rapid wet-to-dry transition."""
        if spi_series.empty or len(spi_series) < 12:
            return {"detected": False, "months_since_wet": None}

        try:
            recent_12 = spi_series.tail(12)["spi"].values

            wet_indices = np.where(recent_12 > 1.5)[0]
            if len(wet_indices) == 0:
                return {"detected": False, "months_since_wet": None}

            last_wet_idx = wet_indices[-1]
            months_since = len(recent_12) - 1 - last_wet_idx

            current_dry = recent_12[-1] < -1.5

            return {
                "detected": current_dry and months_since < 12,
                "months_since_wet": months_since if current_dry else None,
            }
        except Exception:
            return {"detected": False, "months_since_wet": None}
