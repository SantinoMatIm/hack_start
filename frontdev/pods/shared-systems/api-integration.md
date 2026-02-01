# API Integration Guide

**Shared Systems Pod — Frontend Decision Intelligence Organization**

---

## Purpose

This document defines patterns for API integration in the frontend.

---

## API Client

**Location**: `dashboard/utils/api_client.py`

### Getting the Client

```python
from utils.api_client import get_api_client

api = get_api_client()
```

### Available Methods

| Method | Endpoint | Returns |
|--------|----------|---------|
| `get_current_risk(zone_id)` | GET `/risk/current` | Risk assessment dict |
| `get_risk_history(zone_id, days)` | GET `/risk/history` | Historical data dict |
| `get_zones()` | GET `/zones` | List of zones |
| `get_recommended_actions(zone_id, profile)` | POST `/actions/recommended` | Actions dict |
| `run_simulation(zone_id, profile, action_codes, projection_days)` | POST `/scenarios/simulate` | Simulation dict |

---

## Error Handling Pattern

### Standard Pattern

```python
api = get_api_client()

with st.spinner("Loading..."):
    data = api.get_current_risk(zone_id)

if not data or "error" in data:
    st.error("Unable to fetch data. Please ensure the API is running.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Retry"):
            st.rerun()
    with col2:
        if st.button("Show Demo Data"):
            data = get_demo_data()
            st.info("📊 Showing demo data")
    
    if not data:
        return
```

### Error Types

| Error | Handling |
|-------|----------|
| Connection error | Show retry option + demo mode |
| Timeout | Show retry option |
| 404 | Check zone/endpoint validity |
| 500 | Show error message, offer retry |

---

## Demo Mode

### When Demo Mode Activates

- API URL not configured
- API not responding
- User explicitly requests demo

### Demo Data Location

Keep demo data centralized:

```python
# utils/demo_data.py (proposed)

DEMO_RISK = {
    "cdmx": {
        "zone_id": "cdmx",
        "spi_6m": -1.72,
        "risk_level": "HIGH",
        "trend": "WORSENING",
        "days_to_critical": 24,
        "calculated_at": "2024-01-15T10:30:00Z"
    },
    "monterrey": {...}
}

DEMO_ACTIONS = [...]
DEMO_SIMULATION = {...}
```

### Demo Mode Indicator

Always show when using demo data:

```python
st.info("📊 Displaying demo data. Connect to API for live results.")
```

---

## Request Patterns

### GET Request

```python
def get_current_risk(self, zone_id: str) -> dict:
    """Fetch current risk assessment."""
    try:
        response = self.client.get(
            f"{self.base_url}/risk/current",
            params={"zone_id": zone_id},
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

### POST Request

```python
def get_recommended_actions(self, zone_id: str, profile: str) -> dict:
    """Fetch recommended actions."""
    try:
        response = self.client.post(
            f"{self.base_url}/actions/recommended",
            json={"zone_id": zone_id, "profile": profile},
            timeout=15.0
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

---

## Caching

### When to Cache

- Historical data (changes infrequently)
- Zone list (static)
- Action catalog (static)

### How to Cache

```python
@st.cache_data(ttl=300)  # 5 minute cache
def fetch_risk_history(zone_id: str, days: int) -> dict:
    api = get_api_client()
    return api.get_risk_history(zone_id, days)
```

### When NOT to Cache

- Current risk (needs to be live)
- Simulation results (per-request)
- Recommended actions (depend on current state)

---

## Response Contracts

### Risk Current

```json
{
    "zone_id": "cdmx",
    "spi_6m": -1.72,
    "risk_level": "HIGH",
    "trend": "WORSENING",
    "days_to_critical": 24,
    "calculated_at": "2024-01-15T10:30:00Z"
}
```

### Recommended Actions

```json
{
    "zone_id": "cdmx",
    "profile": "government",
    "actions": [
        {
            "base_action_id": "H4_LAWN_BAN",
            "code": "H4_LAWN_BAN",
            "title": "Lawn/Garden Irrigation Restriction",
            "parameters": {
                "reduction_percentage": 15.0,
                "duration_days": 30,
                "priority_level": "HIGH"
            },
            "justification": "...",
            "expected_effect": "+19 days to critical"
        }
    ]
}
```

### Simulation

```json
{
    "zone_id": "cdmx",
    "profile": "government",
    "current_spi": -1.72,
    "no_action_scenario": {
        "projected_spi": -2.12,
        "projected_risk_level": "CRITICAL",
        "days_to_critical": 24,
        "description": "..."
    },
    "with_action_scenario": {
        "projected_spi": -1.87,
        "projected_risk_level": "HIGH",
        "days_to_critical": 52,
        "description": "..."
    },
    "actions_applied": [...],
    "total_days_gained": 28,
    "projection_days": 90
}
```

---

## API Health Check

```python
def check_api_health() -> bool:
    """Check if API is responding."""
    try:
        response = self.client.get(f"{self.base_url}/health", timeout=5.0)
        return response.status_code == 200
    except:
        return False
```

---

*Consistent API integration ensures reliable data flow.*
