"""Ingestion orchestrator for coordinating climate data collection."""

from datetime import date, datetime, timedelta
from typing import Optional
import uuid

from sqlalchemy.orm import Session
import pandas as pd

from src.ingestion.openmeteo_source import OpenMeteoClient
from src.ingestion.noaa_source import NOAAClient
from src.db.models import Zone, ClimateTimeseries


class IngestionOrchestrator:
    """Orchestrates climate data ingestion from multiple sources."""

    def __init__(
        self,
        session: Session,
        openmeteo_client: Optional[OpenMeteoClient] = None,
        noaa_client: Optional[NOAAClient] = None,
    ):
        self.session = session
        self.openmeteo = openmeteo_client or OpenMeteoClient()
        self.noaa = noaa_client or NOAAClient()

    def get_zone_by_slug(self, slug: str) -> Optional[Zone]:
        """Get zone by slug identifier."""
        return self.session.query(Zone).filter(Zone.slug == slug).first()

    def get_last_ingestion_date(
        self,
        zone_id: uuid.UUID,
        source: str,
        variable: str = "precipitation",
    ) -> Optional[date]:
        """Get the most recent ingestion date for a zone/source combination."""
        result = (
            self.session.query(ClimateTimeseries.date)
            .filter(
                ClimateTimeseries.zone_id == zone_id,
                ClimateTimeseries.source == source,
                ClimateTimeseries.variable == variable,
            )
            .order_by(ClimateTimeseries.date.desc())
            .first()
        )
        return result[0] if result else None

    def _normalize_precipitation_data(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Normalize precipitation data to standard format.

        Ensures:
        - Date column is datetime
        - Precipitation values are floats
        - No negative values
        - Missing dates filled with 0
        """
        if df.empty:
            return df

        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df["precipitation_mm"] = df["precipitation_mm"].astype(float).clip(lower=0)

        # Create complete date range
        date_range = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
        df = df.set_index("date").reindex(date_range).fillna(0).reset_index()
        df.columns = ["date", "precipitation_mm"]

        return df

    def _store_timeseries(
        self,
        zone_id: uuid.UUID,
        df: pd.DataFrame,
        source: str,
        variable: str = "precipitation",
    ) -> int:
        """
        Store timeseries data in database.

        Uses upsert logic to handle duplicates.

        Returns:
            Number of records stored
        """
        if df.empty:
            return 0

        stored_count = 0

        for _, row in df.iterrows():
            # Check for existing record
            existing = (
                self.session.query(ClimateTimeseries)
                .filter(
                    ClimateTimeseries.zone_id == zone_id,
                    ClimateTimeseries.variable == variable,
                    ClimateTimeseries.date == row["date"].date(),
                    ClimateTimeseries.source == source,
                )
                .first()
            )

            if existing:
                # Update existing record
                existing.value = row["precipitation_mm"]
            else:
                # Create new record
                record = ClimateTimeseries(
                    zone_id=zone_id,
                    variable=variable,
                    date=row["date"].date(),
                    value=row["precipitation_mm"],
                    source=source,
                )
                self.session.add(record)
                stored_count += 1

        self.session.commit()
        return stored_count

    def ingest_zone_openmeteo(
        self,
        zone: Zone,
        years: int = 30,
        force_full: bool = False,
    ) -> dict:
        """
        Ingest precipitation data from Open-Meteo for a zone.

        Args:
            zone: Zone model instance
            years: Years of historical data to fetch
            force_full: Force full history fetch even if data exists

        Returns:
            Dict with ingestion results
        """
        source = "openmeteo"
        last_date = self.get_last_ingestion_date(zone.id, source)

        if force_full or last_date is None:
            # Full historical fetch
            print(f"Fetching full {years}-year history for {zone.slug} from Open-Meteo...")
            df = self.openmeteo.fetch_full_history(
                zone.latitude, zone.longitude, years=years
            )
        else:
            # Incremental fetch from last date
            start_date = last_date + timedelta(days=1)
            end_date = date.today() - timedelta(days=1)

            if start_date >= end_date:
                return {"zone": zone.slug, "source": source, "records_added": 0, "status": "up_to_date"}

            print(f"Fetching incremental data for {zone.slug} from {start_date} to {end_date}...")
            df = self.openmeteo.fetch_historical_precipitation(
                zone.latitude, zone.longitude, start_date, end_date
            )

        df = self._normalize_precipitation_data(df)
        records_added = self._store_timeseries(zone.id, df, source)

        return {
            "zone": zone.slug,
            "source": source,
            "records_added": records_added,
            "date_range": f"{df['date'].min().date()} to {df['date'].max().date()}" if not df.empty else None,
            "status": "success",
        }

    def ingest_zone_noaa(
        self,
        zone: Zone,
        years: int = 30,
        force_full: bool = False,
    ) -> dict:
        """
        Ingest precipitation data from NOAA for a zone.

        Args:
            zone: Zone model instance
            years: Years of historical data to fetch
            force_full: Force full history fetch

        Returns:
            Dict with ingestion results
        """
        source = "noaa"
        last_date = self.get_last_ingestion_date(zone.id, source)

        end_date = date.today() - timedelta(days=1)
        start_date = date(end_date.year - years, 1, 1)

        if not force_full and last_date:
            start_date = last_date + timedelta(days=1)

        if start_date >= end_date:
            return {"zone": zone.slug, "source": source, "records_added": 0, "status": "up_to_date"}

        print(f"Fetching NOAA data for {zone.slug} from {start_date} to {end_date}...")

        # Use state_code for US zones, otherwise use coordinates
        if zone.country_code == "USA" and zone.state_code:
            print(f"Using state-based lookup for {zone.state_code}...")
            df = self.noaa.fetch_state_precipitation(
                zone.state_code, start_date, end_date, min_years=years
            )
        else:
            df = self.noaa.fetch_historical_precipitation(
                zone.latitude, zone.longitude, start_date, end_date
            )

        df = self._normalize_precipitation_data(df)
        records_added = self._store_timeseries(zone.id, df, source)

        return {
            "zone": zone.slug,
            "source": source,
            "records_added": records_added,
            "date_range": f"{df['date'].min().date()} to {df['date'].max().date()}" if not df.empty else None,
            "status": "success" if records_added > 0 else "no_data",
        }

    def ingest_all_zones(
        self,
        sources: list[str] = ["openmeteo"],
        years: int = 30,
        force_full: bool = False,
    ) -> list[dict]:
        """
        Ingest data for all zones from specified sources.

        Args:
            sources: List of data sources to use
            years: Years of history to fetch
            force_full: Force full history fetch

        Returns:
            List of ingestion results
        """
        zones = self.session.query(Zone).all()
        results = []

        for zone in zones:
            if "openmeteo" in sources:
                result = self.ingest_zone_openmeteo(zone, years, force_full)
                results.append(result)

            if "noaa" in sources:
                result = self.ingest_zone_noaa(zone, years, force_full)
                results.append(result)

        return results

    def get_precipitation_series(
        self,
        zone_id: uuid.UUID,
        source: str = "openmeteo",
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        Get precipitation timeseries for a zone.

        Args:
            zone_id: Zone UUID
            source: Data source name
            start_date: Optional start date filter
            end_date: Optional end date filter

        Returns:
            DataFrame with date and precipitation columns
        """
        query = (
            self.session.query(ClimateTimeseries)
            .filter(
                ClimateTimeseries.zone_id == zone_id,
                ClimateTimeseries.source == source,
                ClimateTimeseries.variable == "precipitation",
            )
        )

        if start_date:
            query = query.filter(ClimateTimeseries.date >= start_date)
        if end_date:
            query = query.filter(ClimateTimeseries.date <= end_date)

        query = query.order_by(ClimateTimeseries.date)

        records = query.all()

        if not records:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        df = pd.DataFrame([
            {"date": r.date, "precipitation_mm": r.value}
            for r in records
        ])

        return df
