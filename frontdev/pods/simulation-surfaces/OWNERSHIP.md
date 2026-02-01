# Simulation Surfaces Pod - Ownership Map

**Frontend Decision Intelligence Engineering Organization**

---

## File Ownership

### Primary Ownership

| File | Ownership Level | Notes |
|------|-----------------|-------|
| `dashboard/pages/3_simulation.py` | **Full** | Primary pod page |
| `dashboard/components/simulation_chart.py` | **Full** | All simulation components |

### Shared Ownership

| File | Shared With | Coordination Notes |
|------|-------------|-------------------|
| `dashboard/assets/styles.css` | Shared Systems | Comparison layout, delta styles |
| `dashboard/utils/api_client.py` | Shared Systems | Simulation API methods |

---

## Component Ownership

### Fully Owned Components

```
simulation_chart.py:
├── render_simulation_comparison()  # Side-by-side comparison
├── render_projection_chart()       # Timeline projection
├── render_impact_breakdown()       # Per-action breakdown
└── render_decision_summary()       # Final CTA section
```

---

## Session State Keys

### Keys We Own

| Key | Type | Description |
|-----|------|-------------|
| `simulation_result` | dict \| None | Results from simulation API |

### Keys We Read

| Key | Owner | Our Usage |
|-----|-------|-----------|
| `selected_zone` | Shared Systems | Display context |
| `selected_profile` | Shared Systems | Display context |
| `selected_actions` | Action Surfaces | Actions to simulate |
| `current_risk` | Risk Surfaces | Risk context display |

---

## API Endpoints

### Endpoints We Call

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/scenarios/simulate` | POST | Run simulation |

### Response Contract

```python
# Request
{
    "zone_id": str,
    "action_codes": list[str],  # Optional, defaults to all recommended
    "projection_days": int
}

# Response
{
    "zone_id": str,
    "profile": str,
    "current_spi": float,
    "no_action_scenario": {
        "projected_spi": float,
        "projected_risk_level": str,
        "days_to_critical": int,
        "description": str
    },
    "with_action_scenario": {
        "projected_spi": float,
        "projected_risk_level": str,
        "days_to_critical": int,
        "description": str
    },
    "actions_applied": [
        {
            "code": str,
            "title": str,
            "days_gained": int
        }
    ],
    "total_days_gained": int,
    "projection_days": int
}
```

---

## CSS Classes

### Classes We Own

| Class | Purpose |
|-------|---------|
| `.comparison-container` | Grid container for comparison |
| `.comparison-card` | Individual scenario card |
| `.comparison-card.no-action` | No-action styling |
| `.comparison-card.with-action` | With-action styling (dark) |
| `.comparison-label` | Scenario label |
| `.delta-positive` | Positive change indicator |
| `.delta-negative` | Negative change indicator |

---

## Change Protocols

### When Simulation Surfaces Pod Can Act Alone

- Bug fixes in owned files
- Improving chart clarity
- Enhancing comparison layout
- Adding methodology explanations

### When Coordination Required

| Change | Coordinate With |
|--------|-----------------|
| Changes to `simulation_result` structure | API consumers |
| New comparison patterns | Design Council |
| Decision confirmation flow | Core Council |

---

*Clear ownership enables autonomous action within boundaries.*
