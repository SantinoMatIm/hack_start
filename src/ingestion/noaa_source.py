"""NOAA API client for validated historical precipitation data."""

from datetime import date, timedelta
from typing import Optional
import httpx
import pandas as pd


class NOAAClient:
    """Client for fetching precipitation data from NOAA Climate Data Online."""

    BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2"

    def __init__(self, api_token: Optional[str] = None, timeout: int = 30):
        """
        Initialize NOAA client.

        Args:
            api_token: NOAA CDO API token (optional, rate limited without it)
            timeout: Request timeout in seconds
        """
        self.api_token = api_token
        self.timeout = timeout

    def _get_headers(self) -> dict:
        """Get request headers with optional API token."""
        headers = {"Accept": "application/json"}
        if self.api_token:
            headers["token"] = self.api_token
        return headers

    def find_nearest_station(
        self,
        latitude: float,
        longitude: float,
        dataset_id: str = "GHCND",
    ) -> Optional[str]:
        """
        Find nearest weather station to given coordinates.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            dataset_id: NOAA dataset ID (default: Global Historical Climatology Network)

        Returns:
            Station ID or None if not found
        """
        # Define a bounding box around the location
        extent = 0.5  # degrees
        bbox = f"{latitude-extent},{longitude-extent},{latitude+extent},{longitude+extent}"

        params = {
            "datasetid": dataset_id,
            "extent": bbox,
            "limit": 10,
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(
                    f"{self.BASE_URL}/stations",
                    params=params,
                    headers=self._get_headers(),
                )
                response.raise_for_status()
                data = response.json()

            if "results" not in data or not data["results"]:
                return None

            # Return first station (usually closest)
            return data["results"][0]["id"]

        except Exception as e:
            print(f"Warning: Failed to find NOAA station: {e}")
            return None

    def fetch_precipitation(
        self,
        station_id: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        Fetch daily precipitation data from NOAA station.

        Args:
            station_id: NOAA station identifier
            start_date: Start date for data fetch
            end_date: End date for data fetch

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        params = {
            "datasetid": "GHCND",
            "stationid": station_id,
            "startdate": start_date.isoformat(),
            "enddate": end_date.isoformat(),
            "datatypeid": "PRCP",  # Precipitation
            "units": "metric",
            "limit": 1000,
        }

        all_data = []
        offset = 1

        try:
            with httpx.Client(timeout=self.timeout) as client:
                while True:
                    params["offset"] = offset
                    response = client.get(
                        f"{self.BASE_URL}/data",
                        params=params,
                        headers=self._get_headers(),
                    )
                    response.raise_for_status()
                    data = response.json()

                    if "results" not in data or not data["results"]:
                        break

                    all_data.extend(data["results"])

                    if len(data["results"]) < 1000:
                        break

                    offset += 1000

        except Exception as e:
            print(f"Warning: Failed to fetch NOAA data: {e}")
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        if not all_data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        df = pd.DataFrame(all_data)
        df["date"] = pd.to_datetime(df["date"])
        df["precipitation_mm"] = df["value"] / 10  # NOAA reports in tenths of mm

        return df[["date", "precipitation_mm"]]

    def fetch_historical_precipitation(
        self,
        latitude: float,
        longitude: float,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        Fetch historical precipitation data for a location.

        First finds nearest station, then fetches data.

        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date
            end_date: End date

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        station_id = self.find_nearest_station(latitude, longitude)

        if not station_id:
            print("Warning: No NOAA station found near location")
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        # NOAA API has 1-year limit per request
        all_data = []
        current_start = start_date

        while current_start < end_date:
            current_end = min(
                date(current_start.year, 12, 31),
                end_date
            )

            chunk = self.fetch_precipitation(station_id, current_start, current_end)
            if not chunk.empty:
                all_data.append(chunk)

            current_start = date(current_start.year + 1, 1, 1)

        if not all_data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        result = pd.concat(all_data, ignore_index=True)
        result = result.drop_duplicates(subset=["date"]).sort_values("date")

        return result
