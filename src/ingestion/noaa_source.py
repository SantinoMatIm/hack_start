"""NOAA API client for validated historical precipitation data."""

from datetime import date, timedelta
from typing import Optional
import httpx
import pandas as pd


# US State FIPS codes for NOAA API
US_STATE_FIPS = {
    "AL": "01", "AK": "02", "AZ": "04", "AR": "05", "CA": "06",
    "CO": "08", "CT": "09", "DE": "10", "FL": "12", "GA": "13",
    "HI": "15", "ID": "16", "IL": "17", "IN": "18", "IA": "19",
    "KS": "20", "KY": "21", "LA": "22", "ME": "23", "MD": "24",
    "MA": "25", "MI": "26", "MN": "27", "MS": "28", "MO": "29",
    "MT": "30", "NE": "31", "NV": "32", "NH": "33", "NJ": "34",
    "NM": "35", "NY": "36", "NC": "37", "ND": "38", "OH": "39",
    "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45",
    "SD": "46", "TN": "47", "TX": "48", "UT": "49", "VT": "50",
    "VA": "51", "WA": "53", "WV": "54", "WI": "55", "WY": "56",
    "DC": "11", "PR": "72",
}


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

    def find_stations_by_state(
        self,
        state_code: str,
        dataset_id: str = "GHCND",
        limit: int = 25,
    ) -> list[dict]:
        """
        Find weather stations in a US state.

        Args:
            state_code: US state code (e.g., "TX", "CA")
            dataset_id: NOAA dataset ID
            limit: Maximum number of stations to return

        Returns:
            List of station info dicts with id, name, mindate, maxdate
        """
        fips = US_STATE_FIPS.get(state_code.upper())
        if not fips:
            print(f"Warning: Unknown state code: {state_code}")
            return []

        params = {
            "datasetid": dataset_id,
            "locationid": f"FIPS:{fips}",
            "datatypeid": "PRCP",  # Only stations with precipitation data
            "limit": limit,
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
                return []

            # Return stations sorted by data coverage (prefer stations with more history)
            stations = []
            for s in data["results"]:
                stations.append({
                    "id": s["id"],
                    "name": s.get("name", ""),
                    "mindate": s.get("mindate", ""),
                    "maxdate": s.get("maxdate", ""),
                    "latitude": s.get("latitude"),
                    "longitude": s.get("longitude"),
                })

            return stations

        except Exception as e:
            print(f"Warning: Failed to find NOAA stations for state {state_code}: {e}")
            return []

    def find_best_station_for_state(
        self,
        state_code: str,
        min_years: int = 30,
    ) -> Optional[str]:
        """
        Find the best station in a state with at least min_years of data.

        Args:
            state_code: US state code
            min_years: Minimum years of historical data required

        Returns:
            Station ID or None
        """
        from datetime import datetime

        stations = self.find_stations_by_state(state_code, limit=50)

        if not stations:
            return None

        # Find station with longest history
        best_station = None
        best_coverage = 0

        target_min_date = date.today().year - min_years

        for station in stations:
            try:
                min_year = int(station["mindate"][:4]) if station["mindate"] else 9999
                max_year = int(station["maxdate"][:4]) if station["maxdate"] else 0

                # Check if station has enough history
                if min_year <= target_min_date:
                    coverage = max_year - min_year
                    if coverage > best_coverage:
                        best_coverage = coverage
                        best_station = station["id"]
            except (ValueError, TypeError):
                continue

        return best_station

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

    def fetch_state_precipitation(
        self,
        state_code: str,
        start_date: date,
        end_date: date,
        min_years: int = 30,
    ) -> pd.DataFrame:
        """
        Fetch historical precipitation data for a US state.

        Finds the best station in the state and fetches data.

        Args:
            state_code: US state code (e.g., "TX", "CA")
            start_date: Start date
            end_date: End date
            min_years: Minimum years of data required from station

        Returns:
            DataFrame with columns: date, precipitation_mm
        """
        station_id = self.find_best_station_for_state(state_code, min_years)

        if not station_id:
            print(f"Warning: No suitable NOAA station found for state {state_code}")
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        print(f"Using NOAA station {station_id} for state {state_code}")

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
                print(f"  Fetched {len(chunk)} records for {current_start.year}")

            current_start = date(current_start.year + 1, 1, 1)

        if not all_data:
            return pd.DataFrame(columns=["date", "precipitation_mm"])

        result = pd.concat(all_data, ignore_index=True)
        result = result.drop_duplicates(subset=["date"]).sort_values("date")

        return result
