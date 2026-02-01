# Risk Surfaces Pod - Ownership Map

**Frontend Decision Intelligence Engineering Organization**

---

## File Ownership

### Primary Ownership

| File | Ownership Level | Notes |
|------|-----------------|-------|
| `dashboard/pages/1_risk_overview.py` | **Full** | Primary pod page |
| `dashboard/components/risk_display.py` | **Full** | All risk display components |

### Shared Ownership

| File | Shared With | Coordination Notes |
|------|-------------|-------------------|
| `dashboard/app.py` | All pods | Zone/profile selection affects risk display |
| `dashboard/assets/styles.css` | Shared Systems | Risk color tokens, gauge styling |
| `dashboard/utils/api_client.py` | Shared Systems | Risk API methods |

### Consumer (Read-Only)

| File | What We Use |
|------|-------------|
| `dashboard/components/header.py` | Header rendering, zone selector |

---

## Component Ownership

### Fully Owned Components

```
risk_display.py:
├── render_risk_card()        # Main risk summary card
├── render_risk_gauge()       # SPI gauge visualization  
├── render_risk_metrics()     # Key metrics row
└── render_risk_explanation() # Contextual explanation
```

### Shared Components We Use

| Component | Owner | Our Usage |
|-----------|-------|-----------|
| `render_header()` | Shared Systems | Page headers |
| `render_zone_selector()` | Shared Systems | Sidebar selection |
| `render_back_button()` | Shared Systems | Navigation |

---

## Session State Keys

### Keys We Own

| Key | Type | Description |
|-----|------|-------------|
| `current_risk` | dict \| None | Latest risk data from API |

### Keys We Read

| Key | Owner | Our Usage |
|-----|-------|-----------|
| `selected_zone` | Shared Systems | Determine which zone to fetch |
| `selected_profile` | Shared Systems | May affect display emphasis |

### Keys We Write For Others

| Key | Consumer | Purpose |
|-----|----------|---------|
| `current_risk` | Action Surfaces, Simulation | Pass risk context forward |

---

## API Endpoints

### Endpoints We Call

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/risk/current?zone_id={zone}` | GET | Fetch current risk assessment |
| `/risk/history?zone_id={zone}&days={n}` | GET | Fetch historical risk data |

### Response Contracts

```python
# /risk/current response
{
    "zone_id": str,
    "spi_6m": float,
    "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
    "trend": "IMPROVING" | "STABLE" | "WORSENING",
    "days_to_critical": int,
    "calculated_at": str  # ISO timestamp
}

# /risk/history response
{
    "zone_id": str,
    "history": [
        {
            "date": str,
            "spi_6m": float,
            "risk_level": str
        }
    ]
}
```

---

## CSS Classes

### Classes We Own

| Class | Purpose | File |
|-------|---------|------|
| `.risk-card` | Risk card container | styles.css |
| `.risk-card.critical` | Critical state styling | styles.css |
| `.risk-card.high` | High state styling | styles.css |
| `.risk-card.medium` | Medium state styling | styles.css |
| `.risk-card.low` | Low state styling | styles.css |
| `.spi-gauge` | SPI gauge container | styles.css |
| `.spi-marker` | Gauge current position marker | styles.css |
| `.metric-container` | Metric display wrapper | styles.css |
| `.metric-value` | Metric value styling | styles.css |
| `.metric-label` | Metric label styling | styles.css |

### Shared Classes We Use

| Class | Owner | Our Usage |
|-------|-------|-----------|
| `.section` | Shared Systems | Section wrapper |
| `.reveal`, `.fade-up` | Shared Systems | Animations |
| `.dark-section` | Shared Systems | CTA sections |

---

## Change Protocols

### When Risk Surfaces Pod Can Act Alone

- Bug fixes in owned files
- Internal refactoring that doesn't change interfaces
- Improving owned components' internal logic
- Adding new components within scope

### When Coordination Required

| Change | Coordinate With |
|--------|-----------------|
| New session state keys | All pods |
| Changes to `current_risk` structure | Action, Simulation pods |
| New CSS classes | Shared Systems (design tokens) |
| New API endpoint usage | Backend team |
| Accessibility changes | Accessibility specialist |

### When Escalation Required

| Change | Escalate To |
|--------|-------------|
| New risk visualization paradigm | Design Council |
| Changes to risk level definitions | Core Council |
| Performance concerns | Engineering Operations |

---

*Clear ownership enables autonomous action within boundaries.*
