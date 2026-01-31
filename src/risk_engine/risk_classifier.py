"""Risk classifier based on SPI-6 values."""

from typing import Optional
from datetime import datetime
import uuid

from sqlalchemy.orm import Session

from src.config.constants import RiskLevel, Trend, classify_risk_level
from src.db.models import Zone, RiskSnapshot
from src.risk_engine.spi_calculator import SPICalculator
from src.risk_engine.trend_analyzer import TrendAnalyzer
from src.risk_engine.critical_estimator import CriticalEstimator


class RiskClassifier:
    """
    Classify drought risk based on SPI-6 and generate risk snapshots.

    Risk Levels:
    - LOW: SPI > -0.5
    - MEDIUM: -1.0 < SPI <= -0.5
    - HIGH: -1.5 < SPI <= -1.0
    - CRITICAL: SPI <= -1.5
    """

    def __init__(
        self,
        session: Optional[Session] = None,
        spi_calculator: Optional[SPICalculator] = None,
        trend_analyzer: Optional[TrendAnalyzer] = None,
        critical_estimator: Optional[CriticalEstimator] = None,
    ):
        self.session = session
        self.spi_calc = spi_calculator or SPICalculator()
        self.trend = trend_analyzer or TrendAnalyzer()
        self.critical_est = critical_estimator or CriticalEstimator()

    def classify(self, spi: float) -> RiskLevel:
        """
        Classify risk level based on SPI value.

        Args:
            spi: SPI-6 value

        Returns:
            RiskLevel enum
        """
        return classify_risk_level(spi)

    def assess_risk(
        self,
        daily_precip,
        zone_id: Optional[uuid.UUID] = None,
        save_snapshot: bool = True,
    ) -> dict:
        """
        Perform full risk assessment for a zone.

        Args:
            daily_precip: DataFrame with precipitation data
            zone_id: Optional zone UUID for saving snapshot
            save_snapshot: Whether to save snapshot to database

        Returns:
            Dictionary with risk assessment results
        """
        # Calculate SPI series
        spi_series = self.spi_calc.calculate_spi(daily_precip)

        if spi_series.empty:
            raise ValueError("Unable to calculate SPI - insufficient data")

        current_spi = spi_series.iloc[-1]["spi"]

        # Classify risk level
        risk_level = self.classify(current_spi)

        # Analyze trend
        trend_result = self.trend.get_trend_summary(spi_series, current_spi)

        # Estimate days to critical
        days_to_critical = self.critical_est.estimate_days_to_critical(
            current_spi=current_spi,
            trend=trend_result["trend"],
            spi_series=spi_series,
        )

        result = {
            "spi_6m": round(current_spi, 2),
            "risk_level": risk_level,
            "trend": trend_result["trend"],
            "days_to_critical": days_to_critical,
            "trend_details": trend_result,
            "last_updated": datetime.utcnow().isoformat(),
        }

        # Save snapshot if requested and session available
        if save_snapshot and self.session and zone_id:
            self._save_snapshot(zone_id, result)

        return result

    def _save_snapshot(self, zone_id: uuid.UUID, assessment: dict) -> RiskSnapshot:
        """Save risk assessment as a snapshot."""
        snapshot = RiskSnapshot(
            zone_id=zone_id,
            spi_6m=assessment["spi_6m"],
            risk_level=assessment["risk_level"].value,
            trend=assessment["trend"].value,
            days_to_critical=assessment["days_to_critical"],
        )
        self.session.add(snapshot)
        self.session.commit()
        return snapshot

    def get_latest_snapshot(self, zone_id: uuid.UUID) -> Optional[RiskSnapshot]:
        """Get the most recent risk snapshot for a zone."""
        if not self.session:
            return None

        return (
            self.session.query(RiskSnapshot)
            .filter(RiskSnapshot.zone_id == zone_id)
            .order_by(RiskSnapshot.created_at.desc())
            .first()
        )

    def get_risk_history(
        self,
        zone_id: uuid.UUID,
        days: int = 30,
    ) -> list[dict]:
        """Get risk snapshot history for a zone."""
        if not self.session:
            return []

        snapshots = (
            self.session.query(RiskSnapshot)
            .filter(RiskSnapshot.zone_id == zone_id)
            .order_by(RiskSnapshot.created_at.desc())
            .limit(days)
            .all()
        )

        return [
            {
                "id": str(s.id),
                "spi_6m": s.spi_6m,
                "risk_level": s.risk_level,
                "trend": s.trend,
                "days_to_critical": s.days_to_critical,
                "created_at": s.created_at.isoformat(),
            }
            for s in snapshots
        ]
