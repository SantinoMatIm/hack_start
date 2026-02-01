# Technical Debt Backlog

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This backlog tracks identified technical debt in the frontend codebase. Technical debt is code that works but could be improved for maintainability, performance, or clarity.

---

## Debt Format

```
## DEBT-{number}: {Title}

**Status**: Identified | In Progress | Resolved | Accepted
**Severity**: Critical | Major | Minor
**Location**: [File(s) affected]

**Description**: [What the debt is]
**Impact**: [How it affects development/users]
**Remediation**: [How to fix it]
**Effort**: Low | Medium | High
**Created**: YYYY-MM-DD
**Resolved**: YYYY-MM-DD (if resolved)
```

---

## Active Debt

### DEBT-001: Repeated CSS Loading

**Status**: Identified
**Severity**: Minor
**Location**: All pages (1_risk_overview.py, 2_actions.py, 3_simulation.py)

**Description**: 
Each page loads CSS file independently with identical code pattern.

**Impact**: 
Code duplication; changes require updating multiple files.

**Remediation**: 
Create shared utility function for CSS loading; import in each page.

**Effort**: Low
**Created**: 2026-01-31

---

### DEBT-002: Session State Key Documentation

**Status**: Identified
**Severity**: Minor
**Location**: All pages

**Description**: 
Session state keys are used but not centrally documented. Keys like `selected_zone`, `current_risk` are spread across files.

**Impact**: 
Risk of key name conflicts; unclear state dependencies.

**Remediation**: 
Create SESSION_STATE_KEYS constant file or documentation; audit all usages.

**Effort**: Medium
**Created**: 2026-01-31

---

### DEBT-003: Demo Data Duplication

**Status**: Identified
**Severity**: Minor
**Location**: 1_risk_overview.py, 2_actions.py, 3_simulation.py

**Description**: 
Demo/fallback data is duplicated across pages when API is unavailable.

**Impact**: 
Inconsistent demo data if values drift; maintenance burden.

**Remediation**: 
Centralize demo data in api_client.py or separate demo_data.py module.

**Effort**: Low
**Created**: 2026-01-31

---

### DEBT-004: Inline HTML Strings

**Status**: Identified
**Severity**: Minor
**Location**: All pages and components

**Description**: 
Large HTML strings embedded in Python code using st.markdown().

**Impact**: 
Hard to read; no syntax highlighting; mixing concerns.

**Remediation**: 
Consider Jinja templates or component-based HTML generation; or accept as Streamlit pattern.

**Effort**: High (may not be worth it)
**Created**: 2026-01-31

---

### DEBT-005: Path Manipulation for Imports

**Status**: Identified
**Severity**: Minor
**Location**: All pages

**Description**: 
Each page uses sys.path.insert() to handle imports from parent directory.

**Impact**: 
Fragile path handling; could break with directory restructuring.

**Remediation**: 
Proper package structure with __init__.py and relative imports; or accept as Streamlit pages pattern.

**Effort**: Medium
**Created**: 2026-01-31

---

## Resolved Debt

*None yet. Resolved debt will be moved here with resolution notes.*

---

## Accepted Debt

*Debt that is acknowledged but intentionally not fixed.*

### DEBT-004: Inline HTML Strings (Accepted)

**Reason for Acceptance**: 
This is a common Streamlit pattern. Moving to templates would add complexity without significant benefit for current scale. May revisit if frontend grows substantially.

**Accepted**: 2026-01-31

---

## Debt Metrics

| Severity | Count | Trend |
|----------|-------|-------|
| Critical | 0 | — |
| Major | 0 | — |
| Minor | 4 active | — |

---

## Debt Priority

Debt should be addressed:
1. When it blocks new work
2. When touching affected code for other reasons
3. During dedicated cleanup sessions
4. Never for its own sake if low impact

---

## How to Add

1. Assign next sequential number
2. Complete all fields
3. Assess severity honestly
4. Add to backlog
5. Update metrics

---

*Technical debt is a tool, not a failure. Track it so it doesn't surprise you.*
