"""
API Client for communicating with the FastAPI backend
"""

import httpx
from typing import Optional
import streamlit as st


class APIClient:
    """HTTP client for the Water Risk Platform API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.timeout = 30.0

    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make a GET request to the API"""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            st.error("Cannot connect to API. Is the backend server running?")
            return {}
        except httpx.HTTPStatusError as e:
            st.error(f"API Error: {e.response.status_code}")
            return {}
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return {}

    def _post(self, endpoint: str, json: Optional[dict] = None) -> dict:
        """Make a POST request to the API"""
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}{endpoint}", json=json)
                response.raise_for_status()
                return response.json()
        except httpx.ConnectError:
            st.error("Cannot connect to API. Is the backend server running?")
            return {}
        except httpx.HTTPStatusError as e:
            st.error(f"API Error: {e.response.status_code}")
            return {}
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return {}

    def health_check(self) -> dict:
        """Check API health status"""
        return self._get("/health")

    def get_zones(self) -> list:
        """Get list of available zones"""
        result = self._get("/zones")
        return result.get("zones", []) if result else []

    def get_current_risk(self, zone_id: str) -> dict:
        """Get current risk assessment for a zone"""
        return self._get("/risk/current", params={"zone_id": zone_id})

    def get_risk_history(self, zone_id: str, days: int = 30) -> dict:
        """Get risk history for a zone"""
        return self._get("/risk/history", params={"zone_id": zone_id, "days": days})

    def get_actions(self) -> list:
        """Get all available base actions"""
        result = self._get("/actions")
        return result.get("actions", []) if result else []

    def get_action(self, code: str) -> dict:
        """Get a specific action by code"""
        return self._get(f"/actions/{code}")

    def get_recommended_actions(self, zone_id: str, profile: str) -> dict:
        """Get AI-recommended actions for a zone and profile"""
        return self._post("/actions/recommended", json={
            "zone_id": zone_id,
            "profile": profile
        })

    def run_simulation(
        self,
        zone_id: str,
        profile: str,
        action_codes: Optional[list] = None,
        projection_days: int = 90
    ) -> dict:
        """Run act vs. not-act simulation"""
        payload = {
            "zone_id": zone_id,
            "profile": profile,
            "projection_days": projection_days
        }
        if action_codes:
            payload["action_codes"] = action_codes
        return self._post("/scenarios/simulate", json=payload)

    def trigger_ingestion(self, zone_id: Optional[str] = None) -> dict:
        """Trigger data ingestion"""
        payload = {}
        if zone_id:
            payload["zone_id"] = zone_id
        return self._post("/ingestion/run", json=payload)


@st.cache_resource
def get_api_client() -> APIClient:
    """Get a cached API client instance"""
    return APIClient()
