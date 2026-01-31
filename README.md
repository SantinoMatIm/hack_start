# Water Risk Platform

**Decision Intelligence Platform for Water Risk (Drought)**

A B2B/B2G platform that transforms climate data into operational decisions. The system prioritizes actions and simulates acting vs. not acting to help manage drought risk.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Dashboard](#dashboard)
- [Decision Heuristics](#decision-heuristics)
- [Action Catalog](#action-catalog)
- [Configuration](#configuration)
- [Development](#development)

---

## Overview

### Problem Statement
- Climate data exists but is not converted into actions
- No prioritization of drought response measures
- No quantified consequences of inaction

### Core Value Proposition
> "Convert climate risk into clear, measurable, operational decisions."

### Pilot Zones
- **Mexico City (CDMX)** - Metropolitan Area
- **Monterrey** - Metropolitan Area

### Key Differentiators
- Action prioritization instead of dashboards
- Simulation of act vs. not-act scenarios
- Controlled, auditable AI (orchestrates decisions, doesn't create policies)
- Parameterized decisions by zone and risk profile
- Business/operational impact focus

---

## Key Features

| Feature | Description |
|---------|-------------|
| **SPI-6 Calculation** | Standardized Precipitation Index using gamma distribution |
| **Risk Classification** | 4-level system (LOW, MEDIUM, HIGH, CRITICAL) |
| **Trend Analysis** | IMPROVING, STABLE, WORSENING detection |
| **Days-to-Critical** | Estimates when SPI reaches critical threshold (-2.0) |
| **6 Heuristic Rules** | Fixed numeric decision logic for action activation |
| **15 Base Actions** | Curated action catalog with parameterizable schemas |
| **AI Orchestration** | OpenAI-powered action parameterization with fallback |
| **Scenario Simulation** | Compare act vs. not-act outcomes |
| **Profile Support** | Government (impact + urgency) vs Industry (impact + cost) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│              Open-Meteo API    +    NOAA API                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Data Ingestion Layer                          │
│         Python jobs for precipitation data collection            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Risk Engine                                 │
│    SPI-6 Calculator → Trend Analyzer → Risk Classifier          │
│                   → Critical Days Estimator                      │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Decision Engine                                │
│    Base Action Catalog → Heuristic Registry                     │
│         → AI Orchestrator → Action Prioritization               │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Simulation Engine                               │
│         Scenario Builder → Delta Calculator                      │
│              Act vs. Not-Act Comparison                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Layer                                   │
│                    FastAPI REST API                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                            │
│                   Streamlit Dashboard                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.10+, FastAPI, Pydantic |
| **Database** | PostgreSQL (Supabase), SQLAlchemy 2.0, Alembic |
| **Data Science** | pandas, numpy, scipy (gamma distribution) |
| **AI** | OpenAI API (GPT-4o-mini) |
| **Climate APIs** | Open-Meteo, NOAA |
| **Frontend** | Streamlit, Plotly |
| **HTTP Client** | httpx |

---

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (optional, demo mode available)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd hack_start

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment example
cp .env.example .env

# Edit .env with your credentials (optional for demo mode)
# DATABASE_URL=postgresql://...
# OPENAI_API_KEY=sk-...
```

### Running the Application

**Option 1: Demo Mode (No Database Required)**

```bash
# Terminal 1: Start API server
.venv/bin/uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Start Dashboard
.venv/bin/streamlit run dashboard/app.py --server.port 8501
```

**Option 2: Using Scripts**

```bash
# Start API
./scripts/run_api.sh

# Start Dashboard
./scripts/run_dashboard.sh
```

### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501
- **API Health**: http://localhost:8000/health

---

## Project Structure

```
water-risk-platform/
├── src/                           # Core application logic
│   ├── api/                       # FastAPI REST endpoints
│   │   ├── main.py               # Application entry point
│   │   ├── routers/              # API route handlers
│   │   │   ├── zones.py          # Zone management
│   │   │   ├── risk.py           # Risk assessment
│   │   │   ├── actions.py        # Action recommendations
│   │   │   ├── scenarios.py      # Simulation endpoints
│   │   │   └── ingestion.py      # Data ingestion
│   │   └── schemas/              # Pydantic models
│   │
│   ├── config/                   # Configuration
│   │   ├── settings.py           # Environment settings
│   │   └── constants.py          # SPI thresholds, profiles
│   │
│   ├── db/                       # Database layer
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   └── connection.py         # Session management
│   │
│   ├── ingestion/                # Climate data acquisition
│   │   ├── orchestrator.py       # Coordinates data collection
│   │   ├── openmeteo_source.py   # Open-Meteo client
│   │   └── noaa_source.py        # NOAA client
│   │
│   ├── risk_engine/              # Risk assessment
│   │   ├── spi_calculator.py     # SPI-6 calculation
│   │   ├── risk_classifier.py    # Risk level classification
│   │   ├── trend_analyzer.py     # Trend detection
│   │   └── critical_estimator.py # Days-to-critical
│   │
│   ├── heuristics/               # Decision rules (6 heuristics)
│   │   ├── base_heuristic.py     # Abstract base class
│   │   ├── h1_industrial_reduction.py
│   │   ├── h2_pressure_management.py
│   │   ├── h3_public_communication.py
│   │   ├── h4_nonessential_restriction.py
│   │   ├── h5_source_reallocation.py
│   │   ├── h6_severity_escalation.py
│   │   └── heuristic_registry.py
│   │
│   ├── actions/                  # Action management
│   │   ├── action_catalog.py     # 15 base actions
│   │   └── prioritization.py     # Scoring logic
│   │
│   ├── simulation/               # Scenario projection
│   │   ├── scenario_builder.py   # Build scenarios
│   │   └── delta_calculator.py   # Calculate impacts
│   │
│   └── ai_orchestrator/          # AI parameterization
│       ├── orchestrator.py       # Main orchestration
│       ├── openai_client.py      # OpenAI API client
│       ├── prompt_templates.py   # Prompt engineering
│       └── fallback_handler.py   # Fallback logic
│
├── dashboard/                     # Streamlit UI
│   ├── app.py                    # Main entry point
│   ├── assets/
│   │   └── styles.css            # Design system
│   ├── components/               # Reusable UI components
│   │   ├── header.py
│   │   ├── risk_display.py
│   │   ├── action_card.py
│   │   └── simulation_chart.py
│   ├── pages/                    # Dashboard pages
│   │   ├── 1_risk_overview.py
│   │   ├── 2_actions.py
│   │   └── 3_simulation.py
│   └── utils/
│       └── api_client.py         # API client
│
├── alembic/                       # Database migrations
├── scripts/                       # Utility scripts
│   ├── run_api.sh
│   ├── run_dashboard.sh
│   ├── init_db.py
│   ├── seed_actions.py
│   └── seed_zones.py
│
├── requirements.txt
├── pyproject.toml
├── alembic.ini
└── .env.example
```

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Health Check
```http
GET /health
```
Returns API status and configuration.

#### Zones
```http
GET /zones
```
List all available zones (CDMX, Monterrey).

```http
GET /zones/{zone_id}
```
Get specific zone details.

#### Risk Assessment
```http
GET /risk/current?zone_id=cdmx
```
**Response:**
```json
{
  "zone_id": "cdmx",
  "spi_6m": -1.72,
  "risk_level": "HIGH",
  "trend": "WORSENING",
  "days_to_critical": 24,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

```http
GET /risk/history?zone_id=cdmx&days=30
```
Get historical risk snapshots.

#### Actions
```http
GET /actions
```
List all 15 base actions.

```http
GET /actions/{action_code}
```
Get specific action details.

```http
POST /actions/recommended
Content-Type: application/json

{
  "zone_id": "cdmx",
  "profile": "government"
}
```
**Response:**
```json
{
  "zone_id": "cdmx",
  "profile": "government",
  "actions": [
    {
      "action_code": "H4_LAWN_BAN",
      "title": "Lawn/Garden Irrigation Restriction",
      "parameters": {
        "reduction_percentage": 15.0,
        "duration_days": 30,
        "priority_level": "HIGH"
      },
      "justification": "SPI -1.72, WORSENING trend...",
      "expected_effect": {
        "days_gained": 19,
        "confidence": "estimated"
      }
    }
  ]
}
```

#### Simulation
```http
POST /scenarios/simulate
Content-Type: application/json

{
  "zone_id": "cdmx",
  "action_codes": ["H4_LAWN_BAN", "H2_PRESSURE_REDUCTION"],
  "projection_days": 90
}
```

---

## Dashboard

### User Flow

1. **Select Zone** - Choose CDMX or Monterrey
2. **Select Profile** - Government or Industry
3. **View Risk** - Current SPI, risk level, trend, days to critical
4. **Review Actions** - AI-parameterized recommendations
5. **Run Simulation** - Compare act vs. not-act scenarios
6. **Make Decision** - Confirm action implementation

### Design System

The dashboard follows a premium, minimal aesthetic:

| Token | Value |
|-------|-------|
| Primary BG | `#F2EDE9` |
| Surface | `#FFFFFF` |
| Dark | `#292929` |
| Accent | `#E76237` |
| Typography | System grotesk sans-serif |
| Shapes | Sharp edges (no border radius) |
| Motion | 800ms ease, scroll reveal animations |

---

## Decision Heuristics

The platform uses 6 fixed numeric heuristics for action selection:

### H1: Moderate Industrial Reduction
- **Trigger**: SPI -1.0 to -1.5, Stable/Worsening, Days > 45
- **Impact**: 5% reduction → +3 days to critical

### H2: Urban Network Pressure Management
- **Trigger**: SPI -1.2 to -1.8, Worsening, Days 30-45
- **Impact**: 10% pressure reduction → +4 days

### H3: Targeted Public Communication
- **Trigger**: SPI -1.0 to -2.0, Worsening, Days > 30
- **Impact**: 3% domestic reduction → +2 days

### H4: Restriction of Non-Essential Uses
- **Trigger**: SPI ≤ -1.8, Worsening, Days < 30
- **Impact**: 1% removed → +1.3 days

### H5: Operational Source Reallocation
- **Trigger**: SPI ≤ -2.0, Stable/Worsening, Days 15-30
- **Impact**: 5% supply increase → +5 days

### H6: Automatic Severity Escalation
- **Trigger**: SPI crosses threshold, Days drop >20% in 2 weeks
- **Impact**: Combined effects × 0.8 (20% penalty)

---

## Action Catalog

15 base actions organized by heuristic:

| Code | Title | Heuristic | Impact |
|------|-------|-----------|--------|
| H1_INDUSTRIAL_AUDIT | Industrial Water Audit | H1 | 5% → +3 days |
| H1_RECYCLING_MANDATE | Recycling Systems | H1 | 10% → +5 days |
| H2_PRESSURE_REDUCTION | Pressure Management | H2 | 10% → +4 days |
| H2_LEAK_DETECTION | Leak Detection | H2 | 1% → +2 days |
| H3_AWARENESS_CAMPAIGN | Public Campaign | H3 | 3% → +2 days |
| H3_SCHOOL_PROGRAM | School Education | H3 | 1% → +0.7 days |
| H3_HOTLINE_LAUNCH | Reporting Hotline | H3 | 0.5% → +0.3 days |
| H4_LAWN_BAN | Lawn Irrigation Ban | H4 | 1% → +1.3 days |
| H4_CARWASH_RESTRICTION | Car Wash Limit | H4 | 0.5% → +0.65 days |
| H4_POOL_RESTRICTION | Pool Filling Ban | H4 | 0.3% → +0.4 days |
| H4_FOUNTAIN_SHUTDOWN | Fountain Shutdown | H4 | 0.2% → +0.26 days |
| H5_EMERGENCY_WELLS | Emergency Wells | H5 | 5% → +5 days |
| H5_TANKER_DEPLOYMENT | Water Tankers | H5 | 2% → +2 days |
| H5_INTERBASIN_TRANSFER | Basin Transfer | H5 | 10% → +10 days |
| H6_EMERGENCY_DECLARATION | Emergency Declaration | H6 | Combined × 0.8 |

---

## Configuration

### Environment Variables

```bash
# Database (Supabase)
DATABASE_URL=postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# OpenAI API (for action parameterization)
OPENAI_API_KEY=sk-...

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development
DEBUG=true
```

### Demo Mode

When `DATABASE_URL` is empty or not set, the API runs in **demo mode** with pre-configured sample data:

- CDMX: SPI -1.72, HIGH risk, WORSENING trend, 24 days to critical
- Monterrey: SPI -1.45, HIGH risk, STABLE trend, 38 days to critical

---

## Development

### Database Setup

```bash
# Run migrations
alembic upgrade head

# Seed initial data
python scripts/init_db.py
python scripts/seed_zones.py
python scripts/seed_actions.py
```

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black src/ dashboard/

# Lint
ruff check src/ dashboard/
```

---

## Risk Levels

| Level | SPI Range | Description |
|-------|-----------|-------------|
| LOW | > -0.5 | Normal conditions |
| MEDIUM | -1.0 to -0.5 | Moderate drought |
| HIGH | -1.5 to -1.0 | Severe drought |
| CRITICAL | ≤ -1.5 | Extreme drought |

---

## Profiles

### Government
- **Priorities**: Impact + Urgency
- **Focus**: Public welfare, rapid response
- **Weights**: Equity, public health

### Industry
- **Priorities**: Impact + Cost
- **Focus**: Cost-effective high-impact solutions
- **Weights**: Economic efficiency, implementation speed

---

## Important Constraints

⚠️ **AI Does NOT**:
- Invent new policies or actions
- Create actions outside the 15-action catalog
- Generate predictions beyond the heuristic formulas

✅ **AI Does**:
- Parametrize actions within allowed ranges
- Adjust percentages, durations, priorities
- Justify decisions numerically
- Fall back to defaults if unavailable

---

## License

Proprietary - All rights reserved

---

## Support

For issues and feature requests, please contact the development team.
