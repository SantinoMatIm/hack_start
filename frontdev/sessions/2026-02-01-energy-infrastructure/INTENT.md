# INTENT

## Session: 2026-02-01-energy-infrastructure

## Current State

The frontend was built for generic water risk assessment with:
- SPI-based risk classification
- Action recommendations for water conservation
- Simulation comparing "no action" vs "with action" in terms of SPI improvement and days gained

The backend has evolved to focus on **energy infrastructure water dependency**:
- Power plants that depend on water for cooling
- Economic costs when water stress reduces plant capacity
- EIA API integration for real electricity/fuel prices
- USD-based cost savings calculations

**Current frontend is disconnected from new backend capabilities.**

## Identified Gaps

| Gap | Impact on Decision-Making | Severity |
|-----|---------------------------|----------|
| Missing economic simulation | Users can't see USD cost/savings impact | Critical |
| No power plant visibility | Users don't see which infrastructure is affected | High |
| No energy price display | Missing context for cost calculations | Medium |
| Outdated messaging | Platform doesn't communicate new value proposition | Medium |
| Missing types/API client | Can't connect to new endpoints | Critical (blocker) |

## Hypotheses

1. If we add economic simulation to the frontend, then decision-makers can see concrete USD savings from taking action, improving decision urgency
2. If we show power plant breakdown, then users understand which specific infrastructure benefits from water actions
3. If we display current energy prices, then cost calculations feel grounded and credible

## Proposed Changes

| Change | Create/Modify/Delete | Rationale |
|--------|---------------------|-----------|
| `types.ts` - Add new interfaces | Modify | Enable TypeScript for new API responses |
| `client.ts` - Add API functions | Modify | Connect to new endpoints |
| Simulation page - Economic results | Modify | Show USD savings, costs, plant breakdown |
| Landing page - Messaging update | Modify | Reflect energy infrastructure focus |
| Power plant components | Create | Display plant data with capacity, type, dependency |

## Risks
- Backend endpoints may not be fully tested
- EIA API unavailable → need robust fallback
- Existing SPI simulation logic may conflict with economic simulation
- Users may be confused by dual simulation modes (SPI vs Economic)

## Implementation Priority

1. **API Layer** (must be first - unblocks everything)
2. **Simulation Page** (highest value - shows USD savings)
3. **Landing Page** (communicates new value prop)
4. **Power Plants Surface** (additional context)

## Approval
- [x] Human approval received to proceed to Phase 2 (user provided context and requested changes)
