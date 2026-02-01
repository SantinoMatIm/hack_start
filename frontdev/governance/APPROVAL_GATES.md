# Approval Gates

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines the approval criteria and gates that must be passed at each phase of a frontend working session. Gates ensure quality, alignment, and decision-support effectiveness.

---

## Gate Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   STARTUP   │────▶│   GATE 1    │────▶│   GATE 2    │────▶│   GATE 3    │
│   COMPLETE  │     │ Intent OK   │     │ Code OK     │     │Fidelity OK  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
 Proceed to          Proceed to          Proceed to          Session
  Phase 1             Phase 2             Phase 3            Complete
```

---

## Gate 0: Startup Completion

### Purpose
Verify that organizational context has been absorbed before any work begins.

### Criteria

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| Governance absorbed | All governance/ files read | Checklist in startup |
| Memory reviewed | All memory/ files scanned | Checklist in startup |
| Sessions checked | In-progress sessions identified | List generated |
| Context established | Codebase context understood | Current state known |
| Issues surfaced | Contradictions/gaps documented | Issues log (if any) |

### Pass Condition
All startup checklist items complete, OR blocking issues escalated.

### Fail Action
Cannot proceed to any phase. Must resolve startup blockers.

---

## Gate 1: Intent Approval

### Purpose
Verify that the proposed changes are well-defined, justified, and approved before implementation begins.

### Criteria

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| Current state documented | What exists now is clear | INTENT.md section |
| Gaps identified | Decision-support gaps named | Gap table in INTENT.md |
| Hypotheses stated | How changes improve decisions | Hypotheses in INTENT.md |
| Changes specified | What will be created/modified/deleted | Changes table |
| Risks identified | Potential problems named | Risk list |
| Human approval | Human confirms intent | Explicit approval |

### INTENT.md Required Sections

```markdown
## Current State
[Description of what exists]

## Identified Gaps
| Gap | Impact | Severity |
|-----|--------|----------|

## Hypotheses
1. If we [change], then [improvement] because [rationale]

## Proposed Changes
| Change | Type | Rationale |
|--------|------|-----------|

## Risks
- [Risk list]

## Approval
- [ ] Human approval to proceed
```

### Pass Condition
- All sections complete
- Hypotheses are testable
- Human explicitly approves

### Fail Action
- Request clarification on gaps
- Refine intent
- Do NOT proceed to Phase 2

---

## Gate 2: Implementation Approval

### Purpose
Verify that code changes are complete, functional, and logged before fidelity review.

### Criteria

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| Code functional | No errors, renders correctly | Test run |
| Integration intact | Works with existing code | Integration test |
| Standards followed | CODE_STANDARDS.md compliance | Code review |
| Design followed | DESIGN_STANDARDS.md compliance | Design review |
| Changes logged | All changes in IMPLEMENTATION_LOG.md | Log check |
| Debt documented | Technical debt logged if incurred | Debt section |

### IMPLEMENTATION_LOG.md Required Sections

```markdown
## Changes Made
### [timestamp] - [summary]
File: [path]
Type: Create | Modify | Delete
Description: [what and why]

## Design Decisions
| Decision | Options | Choice | Rationale |
|----------|---------|--------|-----------|

## Technical Debt
| Item | Reason | Remediation |
|------|--------|-------------|

## Blockers Encountered
| Blocker | Resolution |
|---------|------------|
```

### Pass Condition
- Code runs without errors
- Integrates with existing system
- All changes logged
- Standards compliance verified

### Fail Action
- Fix code issues
- Complete logging
- Do NOT proceed to Phase 3

---

## Gate 3: Fidelity Approval

### Purpose
Verify that the frontend changes meet decision-support standards and are production-ready.

### Criteria

| Criterion | Requirement | Verification |
|-----------|-------------|--------------|
| Accuracy | UI reflects system state correctly | Data comparison |
| Uncertainty | Uncertainty is visible, not hidden | Visual check |
| Consequences | Act vs not-act is clear | User perspective |
| Pressure support | Works under stress conditions | Usability check |
| Accessibility | WCAG AA compliance | A11y check |
| Performance | Meets performance constraints | Load test |
| Integration | Works with full system | E2E check |
| Standards | Code and design standards met | Review |

### FIDELITY_REVIEW.md Required Format

```markdown
## Review Summary
| Criterion | Status | Notes |
|-----------|--------|-------|
| Accuracy | Pass/Fail | |
| Uncertainty | Pass/Fail | |
| Consequences | Pass/Fail | |
| Pressure Support | Pass/Fail | |
| Accessibility | Pass/Fail | |
| Performance | Pass/Fail | |
| Integration | Pass/Fail | |
| Standards | Pass/Fail | |

## Overall Status
[ ] APPROVED
[ ] REVISION REQUIRED
[ ] ROLLBACK REQUIRED

## Issues
| Issue | Severity | Action |
|-------|----------|--------|

## Sign-off
- [ ] Review Board approval
```

### Pass Condition
- All criteria pass OR only minor issues remain
- No critical or major issues unresolved
- Review Board sign-off

### Fail Actions

| Status | Action |
|--------|--------|
| Revision Required | Return to Phase 2, fix issues |
| Rollback Required | Revert changes, document lessons |

---

## Approval Authority

### Gate 0 (Startup)
- **Authority**: Self-assessment
- **Override**: Human can direct to proceed despite gaps

### Gate 1 (Intent)
- **Authority**: Human approval required
- **Override**: None — human must approve intent

### Gate 2 (Implementation)
- **Authority**: Self-assessment with specialist input
- **Override**: Human can accept known issues

### Gate 3 (Fidelity)
- **Authority**: Decision Fidelity Review Board
- **Override**: Human can accept with documented exceptions

---

## Gate Failure Handling

### Soft Failures
Minor issues that don't block progress:
- Document in session artifacts
- Create backlog items
- Proceed with awareness

### Hard Failures
Critical issues that block progress:
- Document failure reason
- Determine remediation path
- Do not proceed until resolved

### Escalation
When gate failure cannot be resolved:
- Follow ESCALATION_POLICY.md
- Document escalation reason
- Await resolution before proceeding

---

## Gate Timing

| Gate | Expected Duration | Timeout Action |
|------|-------------------|----------------|
| Gate 0 | 5-15 minutes | Escalate if blocked |
| Gate 1 | Varies by complexity | Await human response |
| Gate 2 | Varies by scope | Document progress, pause if stuck |
| Gate 3 | 10-20 minutes | Complete review or defer |

---

## Gate Documentation

All gate decisions must be recorded:

### In SESSION_RECORD.md
```markdown
## Gate Status
- Gate 0 (Startup): [Pass/Blocked] - [timestamp]
- Gate 1 (Intent): [Pass/Fail] - [timestamp]
- Gate 2 (Implementation): [Pass/Fail] - [timestamp]
- Gate 3 (Fidelity): [Pass/Fail/Deferred] - [timestamp]
```

### Gate failures become lessons learned
- Document in memory/LESSONS_LEARNED.md
- Identify patterns across sessions
- Improve process based on failures

---

*Gates ensure quality without bureaucracy. They exist to catch problems early, not to slow progress.*
