"""EIA (Energy Information Administration) API client for energy prices."""

from datetime import datetime, timedelta
from typing import Optional
import httpx
import pandas as pd

from src.config.settings import get_settings


class EIAClient:
    """Client for fetching energy prices from EIA Open Data API.

    Used to get:
    - P_marginal: Retail electricity prices (USD/MWh)
    - C_op: Average operational costs by fuel type
    - Emergency fuel prices for cost calculations
    """

    BASE_URL = "https://api.eia.gov/v2"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        """Initialize EIA client.

        Args:
            api_key: EIA API key. If not provided, reads from settings.
            timeout: Request timeout in seconds.
        """
        self.api_key = api_key or get_settings().eia_api_key
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("EIA API key is required. Set EIA_API_KEY in .env")

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """Make authenticated request to EIA API.

        Args:
            endpoint: API endpoint path (e.g., "/electricity/retail-sales/data")
            params: Query parameters

        Returns:
            JSON response as dict
        """
        url = f"{self.BASE_URL}{endpoint}"

        request_params = {"api_key": self.api_key}
        if params:
            request_params.update(params)

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(url, params=request_params)
            response.raise_for_status()
            return response.json()

    def fetch_electricity_prices(
        self,
        state: Optional[str] = None,
        sector: str = "ALL",
    ) -> pd.DataFrame:
        """Fetch retail electricity prices (USD/MWh) - P_marginal.

        Args:
            state: State code (e.g., "TX", "CA"). None for national average.
            sector: Sector ID - ALL, RES (residential), COM (commercial), IND (industrial)

        Returns:
            DataFrame with columns: period, state, sector, price_cents_kwh, price_usd_mwh
        """
        params = {
            "data[0]": "price",
            "facets[sectorid][]": sector,
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "length": 12,  # Last 12 months
        }

        if state:
            params["facets[stateid][]"] = state

        try:
            data = self._make_request("/electricity/retail-sales/data", params)
        except httpx.HTTPStatusError as e:
            print(f"EIA API error: {e}")
            return pd.DataFrame()

        if "response" not in data or "data" not in data["response"]:
            return pd.DataFrame()

        records = data["response"]["data"]

        df = pd.DataFrame(records)

        if df.empty:
            return df

        # Rename and convert units
        # EIA returns cents/kWh, we need USD/MWh
        # 1 cent/kWh = 10 USD/MWh
        if "price" in df.columns:
            df["price_cents_kwh"] = pd.to_numeric(df["price"], errors="coerce")
            df["price_usd_mwh"] = df["price_cents_kwh"] * 10

        return df

    def fetch_natural_gas_prices(self) -> pd.DataFrame:
        """Fetch natural gas spot prices (USD/MMBtu) for emergency fuel costs.

        Returns:
            DataFrame with columns: period, price_usd_mmbtu
        """
        params = {
            "data[0]": "value",
            "facets[series][]": "RNGWHHD",  # Henry Hub Natural Gas Spot Price
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "length": 30,  # Last 30 days
        }

        try:
            data = self._make_request("/natural-gas/pri/fut/data", params)
        except httpx.HTTPStatusError as e:
            print(f"EIA API error: {e}")
            return pd.DataFrame()

        if "response" not in data or "data" not in data["response"]:
            return pd.DataFrame()

        records = data["response"]["data"]
        df = pd.DataFrame(records)

        if df.empty:
            return df

        if "value" in df.columns:
            df["price_usd_mmbtu"] = pd.to_numeric(df["value"], errors="coerce")

        return df

    def fetch_generation_by_fuel(
        self,
        fuel_type: Optional[str] = None,
    ) -> pd.DataFrame:
        """Fetch electricity generation by fuel type.

        Args:
            fuel_type: Fuel type code (e.g., "NG" for natural gas, "COL" for coal)

        Returns:
            DataFrame with generation data by fuel type
        """
        params = {
            "data[0]": "generation",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "length": 12,
        }

        if fuel_type:
            params["facets[fueltypeid][]"] = fuel_type

        try:
            data = self._make_request("/electricity/electric-power-operational-data/data", params)
        except httpx.HTTPStatusError as e:
            print(f"EIA API error: {e}")
            return pd.DataFrame()

        if "response" not in data or "data" not in data["response"]:
            return pd.DataFrame()

        return pd.DataFrame(data["response"]["data"])

    def get_current_prices(self, state: Optional[str] = None) -> dict:
        """Get current prices for economic calculations.

        Args:
            state: US state code (e.g., "TX", "CA") for regional prices.
                   If None, returns national average.

        Returns dict with:
        - marginal_price_usd_mwh: Average retail electricity price
        - fuel_price_usd_mmbtu: Natural gas spot price
        - region: State code or "US" for national
        """
        # Get electricity price (state-specific if provided)
        elec_df = self.fetch_electricity_prices(state=state, sector="ALL")
        marginal_price = 100.0  # Default fallback USD/MWh

        if not elec_df.empty and "price_usd_mwh" in elec_df.columns:
            valid_prices = elec_df["price_usd_mwh"].dropna()
            if len(valid_prices) > 0:
                marginal_price = float(valid_prices.iloc[0])

        # Get natural gas price
        gas_df = self.fetch_natural_gas_prices()
        fuel_price = 3.0  # Default fallback USD/MMBtu

        if not gas_df.empty and "price_usd_mmbtu" in gas_df.columns:
            valid_prices = gas_df["price_usd_mmbtu"].dropna()
            if len(valid_prices) > 0:
                fuel_price = float(valid_prices.iloc[0])

        return {
            "marginal_price_usd_mwh": marginal_price,
            "fuel_price_usd_mmbtu": fuel_price,
            "fetched_at": datetime.utcnow().isoformat(),
            "region": state or "US",
        }
