# Shared Systems Pod Charter

**Frontend Decision Intelligence Engineering Organization**

---

## Mission

Provide consistent, reusable foundations that enable all other pods to build coherent, maintainable decision surfaces.

---

## Scope

### Owned Domains

| Domain | Description |
|--------|-------------|
| Design System | Tokens, typography, colors, spacing, motion |
| Component Library | Shared, reusable components |
| API Integration | API client and data fetching patterns |
| State Management | Session state patterns and conventions |
| Navigation | Global navigation and routing |

### Owned Files

| File | Purpose |
|------|---------|
| `dashboard/assets/styles.css` | Design system implementation |
| `dashboard/utils/api_client.py` | API client abstraction |
| `dashboard/components/header.py` | Shared header components |
| `dashboard/app.py` | Main entry, global structure |

### Cross-Pod Services

| Service | Consumers |
|---------|-----------|
| Design tokens | All pods |
| API client | All pods |
| Header/navigation | All pods |
| Session state keys | All pods |

---

## Key Principles

1. **Consistency Enables Speed**: Shared patterns reduce decisions for other pods
2. **Tokens, Not Values**: Design decisions are tokens, not hardcoded values
3. **Single Source of Truth**: One place for shared concerns
4. **Graceful Degradation**: API client handles errors consistently

---

## Design System

### Token Categories

| Category | Location | Examples |
|----------|----------|----------|
| Colors | CSS :root | --bg-primary, --risk-critical |
| Typography | CSS :root | --font-family, .display-text |
| Spacing | CSS :root | --space-xs through --space-3xl |
| Motion | CSS :root | --duration-default, --ease-default |
| Components | CSS classes | .risk-card, .action-card |

### Design Council Relationship

- Design Council governs token decisions
- Shared Systems implements and maintains
- Changes require Design Council approval

---

## API Client

### Responsibilities

- Centralize all API calls
- Handle errors consistently
- Provide demo mode fallback
- Manage timeouts

### Interface

```python
class APIClient:
    def get_current_risk(self, zone_id: str) -> dict
    def get_risk_history(self, zone_id: str, days: int) -> dict
    def get_recommended_actions(self, zone_id: str, profile: str) -> dict
    def run_simulation(self, zone_id: str, profile: str, 
                       action_codes: list, projection_days: int) -> dict
```

---

## Session State

### Owned Keys

| Key | Type | Owner |
|-----|------|-------|
| `selected_zone` | str | Shared Systems |
| `selected_profile` | str | Shared Systems |

### Key Naming Convention

- snake_case for all keys
- Prefix with context: `selected_`, `current_`, `recommended_`
- Document all keys

---

## Collaboration

### With Other Pods

- Provide stable interfaces
- Announce breaking changes
- Coordinate on new components
- Review token additions

### With Design Council

- Implement token decisions
- Propose token changes
- Maintain design system documentation

---

## Quality Standards

### Must Have

- [ ] All design tokens documented
- [ ] API client handles all endpoints
- [ ] Error handling consistent
- [ ] Demo mode functional
- [ ] Session state keys documented

### Should Have

- [ ] Component library documented
- [ ] Responsive patterns defined
- [ ] Accessibility patterns included

---

## Current State Assessment

### Strengths

- Comprehensive CSS design system
- API client abstraction exists
- Session state pattern established

### Gaps

- Token documentation could be clearer
- Component library not fully documented
- Some patterns duplicated across pods

### Technical Debt

- CSS loading duplicated (DEBT-001)
- Session state keys not centrally documented (DEBT-002)
- Demo data duplicated (DEBT-003)

---

## Pod Roadmap

### Phase 1: Foundation (Current)
- Design tokens ✓
- API client ✓
- Session state ✓

### Phase 2: Documentation
- Document all tokens
- Document all components
- Create pattern library

### Phase 3: Consolidation
- Address technical debt
- Centralize duplicated patterns
- Improve demo mode

---

*Shared Systems is the foundation. Strong foundations enable all other work.*
