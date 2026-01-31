"""Open-Meteo API client for historical and recent precipitation data."""

from datetime import date, timedelta
from typing import Optional
import httpx
import pandas as pd


class OpenMeteoClient:
    """Client for fetching precipitation data from Open-Meteo API."""

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch_historical_precipitation(
        self,
        latitude: float,
        longitude: float,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        Fetch historical daily precipitation data.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date for data fetch
            end_date: End date for data fetch

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": "precipitation_sum",
            "timezone": "America/Mexico_City",
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

        if "daily" not in data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        df = pd.DataFrame({
            "date": pd.to_datetime(data["daily"]["time"]),
            "precipitation_mm": data["daily"]["precipitation_sum"],
        })

        # Handle null values
        df["precipitation_mm"] = df["precipitation_mm"].fillna(0)

        return df

    def fetch_recent_precipitation(
        self,
        latitude: float,
        longitude: float,
        days_back: int = 7,
    ) -> pd.DataFrame:
        """
        Fetch recent precipitation data (last N days).

        Uses forecast API for most recent data that may not be in archive yet.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            days_back: Number of days to look back

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "past_days": days_back,
            "daily": "precipitation_sum",
            "timezone": "America/Mexico_City",
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(self.FORECAST_URL, params=params)
            response.raise_for_status()
            data = response.json()

        if "daily" not in data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        df = pd.DataFrame({
            "date": pd.to_datetime(data["daily"]["time"]),
            "precipitation_mm": data["daily"]["precipitation_sum"],
        })

        # Filter to only past dates
        today = date.today()
        df = df[df["date"].dt.date <= today]
        df["precipitation_mm"] = df["precipitation_mm"].fillna(0)

        return df

    def fetch_full_history(
        self,
        latitude: float,
        longitude: float,
        years: int = 30,
    ) -> pd.DataFrame:
        """
        Fetch full precipitation history for SPI calculation.

        Fetches data in yearly chunks to avoid API limits.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            years: Number of years to fetch

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        end_date = date.today() - timedelta(days=1)
        start_date = date(end_date.year - years, 1, 1)

        all_data = []

        # Fetch in chunks to avoid API timeouts
        current_start = start_date
        while current_start < end_date:
            current_end = min(
                date(current_start.year + 5, 12, 31),
                end_date
            )

            try:
                chunk = self.fetch_historical_precipitation(
                    latitude, longitude, current_start, current_end
                )
                all_data.append(chunk)
            except Exception as e:
                print(f"Warning: Failed to fetch data for {current_start} to {current_end}: {e}")

            current_start = date(current_end.year + 1, 1, 1)

        if not all_data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        result = pd.concat(all_data, ignore_index=True)
        result = result.drop_duplicates(subset=["date"]).sort_values("date")

        return result
