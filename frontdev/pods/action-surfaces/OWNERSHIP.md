# Action Surfaces Pod - Ownership Map

**Frontend Decision Intelligence Engineering Organization**

---

## File Ownership

### Primary Ownership

| File | Ownership Level | Notes |
|------|-----------------|-------|
| `dashboard/pages/2_actions.py` | **Full** | Primary pod page |
| `dashboard/components/action_card.py` | **Full** | All action display components |

### Shared Ownership

| File | Shared With | Coordination Notes |
|------|-------------|-------------------|
| `dashboard/assets/styles.css` | Shared Systems | Action card styling, priority badges |
| `dashboard/utils/api_client.py` | Shared Systems | Action API methods |

### Consumer (Read-Only)

| File | What We Use |
|------|-------------|
| `dashboard/components/header.py` | Header, zone selector |
| `dashboard/components/risk_display.py` | Risk metrics for context |

---

## Component Ownership

### Fully Owned Components

```
action_card.py:
├── render_action_card()          # Individual action card
├── render_action_list()          # Collection of action cards
├── render_action_summary()       # Summary statistics
└── render_heuristic_explanation() # H1-H6 explanations
```

---

## Session State Keys

### Keys We Own

| Key | Type | Description |
|-----|------|-------------|
| `recommended_actions` | list \| None | Actions from API |
| `selected_actions` | list | Action codes selected for simulation |

### Keys We Read

| Key | Owner | Our Usage |
|-----|-------|-----------|
| `selected_zone` | Shared Systems | API call parameter |
| `selected_profile` | Shared Systems | API call parameter, display |
| `current_risk` | Risk Surfaces | Display risk context |

### Keys We Write For Others

| Key | Consumer | Purpose |
|-----|----------|---------|
| `selected_actions` | Simulation Surfaces | Actions to simulate |

---

## API Endpoints

### Endpoints We Call

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/actions/recommended` | POST | Get recommended actions |
| `/actions` | GET | List all available actions |
| `/actions/{action_code}` | GET | Get single action detail |

### Response Contract (`/actions/recommended`)

```python
# Request
{
    "zone_id": str,
    "profile": "government" | "industry"
}

# Response
{
    "zone_id": str,
    "profile": str,
    "actions": [
        {
            "base_action_id": str,
            "code": str,
            "title": str,
            "parameters": {
                "reduction_percentage": float,
                "duration_days": int,
                "priority_level": str,
                # ... varies by action
            },
            "justification": str,
            "expected_effect": str
        }
    ]
}
```

---

## CSS Classes

### Classes We Own

| Class | Purpose |
|-------|---------|
| `.action-card` | Action card container |
| `.action-card:hover` | Hover state |
| `.action-priority` | Priority badge base |
| `.action-priority.high` | High priority styling |
| `.action-priority.medium` | Medium priority styling |
| `.action-priority.low` | Low priority styling |

---

## Change Protocols

### When Action Surfaces Pod Can Act Alone

- Bug fixes in owned files
- Internal refactoring
- Improving action card layout
- Adding heuristic explanations

### When Coordination Required

| Change | Coordinate With |
|--------|-----------------|
| Changes to `selected_actions` structure | Simulation Surfaces |
| New CSS classes | Shared Systems |
| Changes to action card anatomy | Design Council |

---

*Clear ownership enables autonomous action within boundaries.*
