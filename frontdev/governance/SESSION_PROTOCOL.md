# Session Protocol

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This protocol defines how frontend working sessions are initiated, conducted, and concluded. All frontend work occurs through structured sessions.

---

## Session Lifecycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   STARTUP    │────▶│   PHASE 1    │────▶│   PHASE 2    │────▶│   PHASE 3    │
│   PROTOCOL   │     │ Intent/Gaps  │     │Implementation│     │   Fidelity   │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
 Context loaded       INTENT.md           Code changes         FIDELITY_
                      created             + IMPL_LOG.md        REVIEW.md
```

---

## Session Initialization

### 1. Create Session Folder

```
frontdev/sessions/{date}-{focus}/
```

Example: `frontdev/sessions/2026-01-31-urgency-visualization/`

### 2. Create SESSION_RECORD.md

```markdown
# SESSION RECORD

## Metadata
- **Session ID**: {date}-{focus}
- **Date**: {YYYY-MM-DD}
- **Status**: in_progress
- **Frontend Lead**: [Agent]

## Focus
- **Page/Flow/Surface**: {specific target}
- **Target User Profile**: {government | industry | both}
- **Target Decision Context**: {risk level, zone, urgency}

## Constraints
| Category | Constraint |
|----------|------------|
| Technical | {relevant constraints} |
| Governance | {relevant constraints} |
| Accessibility | {relevant constraints} |
| Performance | {relevant constraints} |

## Assumptions (Explicit)
- {assumption 1}
- {assumption 2}

## Open Questions
1. {question needing resolution}
```

---

## Phase 1: Intent & Gaps

### Purpose
Establish what frontend code currently exists, what decision it serves (or fails to serve), and what gaps, weaknesses, or misalignments may exist.

### Activities
1. Review current state of target surface
2. Identify gaps against decision-making goals
3. Challenge assumptions (including human-provided ones)
4. Formulate hypotheses about what changes will improve decisions
5. Document intent

### Success Criteria
- [ ] Current state documented
- [ ] Gaps clearly identified with rationale
- [ ] Hypotheses about improvement stated
- [ ] Intent approved by human before Phase 2

### Output: INTENT.md

```markdown
# INTENT

## Session: {session-id}

## Current State
{Description of what exists now}

## Identified Gaps
| Gap | Impact on Decision-Making | Severity |
|-----|---------------------------|----------|
| {gap 1} | {how it hurts decisions} | High/Med/Low |

## Hypotheses
1. If we {change X}, then {decision improvement Y} because {rationale Z}

## Proposed Changes
| Change | Create/Modify/Delete | Rationale |
|--------|---------------------|-----------|
| {change 1} | {type} | {why} |

## Risks
- {risk 1}
- {risk 2}

## Approval
- [ ] Human approval received to proceed to Phase 2
```

### On Failure
If gaps cannot be clearly identified or intent is ambiguous:
- Request clarification from human
- Do not proceed to Phase 2
- Log blocking reason

---

## Phase 2: Implementation

### Purpose
Write, modify, refactor, or delete frontend code based on the approved intent.

### Activities
1. Implement code changes
2. Ensure integration with existing frontend
3. Ensure API contracts respected
4. Document significant decisions in IMPLEMENTATION_LOG.md
5. Handle human interrupts via `/question` command

### Success Criteria
- [ ] Code compiles/runs without errors
- [ ] Integrates with existing codebase
- [ ] Follows CODE_STANDARDS.md
- [ ] Follows DESIGN_STANDARDS.md
- [ ] All changes logged

### Output: IMPLEMENTATION_LOG.md + Actual Code

```markdown
# IMPLEMENTATION LOG

## Session: {session-id}

## Changes Made

### {timestamp} - {change summary}
**File**: {path}
**Type**: Create | Modify | Delete
**Description**: {what and why}
**Lines affected**: {if modify}

### {timestamp} - {change summary}
...

## Design Decisions During Implementation
| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| {decision} | {options} | {choice} | {why} |

## Technical Debt Introduced
| Item | Reason | Remediation Plan |
|------|--------|------------------|
| {debt} | {why incurred} | {when/how to fix} |

## Blockers Encountered
| Blocker | Resolution |
|---------|------------|
| {blocker} | {how resolved} |
```

### Human Interrupt Protocol

During Phase 2, human may use:

```
/question {text}
```

This:
1. Pauses implementation
2. Addresses the question
3. Logs Q&A in IMPLEMENTATION_LOG.md
4. Resumes work

### On Failure
If implementation cannot proceed:
- Log blocker in IMPLEMENTATION_LOG.md
- Escalate per ESCALATION_POLICY.md
- Do not proceed to Phase 3 with broken code

---

## Phase 3: Fidelity Review

### Purpose
Evaluate whether the resulting frontend code meets decision-support standards and is production-ready.

### Review Criteria

| Criterion | Question | Pass/Fail |
|-----------|----------|-----------|
| **Accuracy** | Does the UI accurately reflect system state? | |
| **Uncertainty** | Is uncertainty visible, not hidden? | |
| **Consequences** | Are act vs not-act consequences clear? | |
| **Pressure Support** | Does it support decision-making under stress? | |
| **Accessibility** | Does it meet WCAG AA? | |
| **Performance** | Does it meet performance constraints? | |
| **Integration** | Does it work with existing code? | |
| **Standards** | Does it follow code and design standards? | |

### Output: FIDELITY_REVIEW.md

```markdown
# FIDELITY REVIEW

## Session: {session-id}

## Review Summary
| Criterion | Status | Notes |
|-----------|--------|-------|
| Accuracy | Pass/Fail | {notes} |
| Uncertainty | Pass/Fail | {notes} |
| Consequences | Pass/Fail | {notes} |
| Pressure Support | Pass/Fail | {notes} |
| Accessibility | Pass/Fail | {notes} |
| Performance | Pass/Fail | {notes} |
| Integration | Pass/Fail | {notes} |
| Standards | Pass/Fail | {notes} |

## Overall Status
[ ] APPROVED - Ready for production
[ ] REVISION REQUIRED - Issues listed below
[ ] ROLLBACK REQUIRED - Critical failures

## Issues Requiring Resolution
| Issue | Severity | Required Action |
|-------|----------|-----------------|
| {issue} | Critical/Major/Minor | {action} |

## Sign-off
- [ ] Decision Fidelity Review Board approval
```

### On Pass
- Update SESSION_RECORD.md status to `completed`
- Move session to completed state
- Update memory/ if architectural or design decisions were made

### On Fail
- Document failures in FIDELITY_REVIEW.md
- Either:
  - Return to Phase 2 for revision
  - Rollback changes
- Log rationale for decision
- Session remains `in_progress` or moves to `revision_required`

---

## Session Status Values

| Status | Meaning |
|--------|---------|
| `in_progress` | Work actively ongoing |
| `awaiting_review` | Phase 3 review pending |
| `revision_required` | Failed review, needs fixes |
| `blocked` | Cannot proceed, awaiting resolution |
| `completed` | All phases passed |
| `aborted` | Terminated with rationale |

---

## Session Commands

| Command | Effect |
|---------|--------|
| `/question {text}` | Pause, address question, resume |
| `/status` | Display current session state |
| `/debate` | Surface internal specialist disagreement |
| `/adversary` | Invoke devil's advocate review |
| `/abort` | Terminate session with logged rationale |

---

## Session Artifact Checklist

Every completed session should have:

- [ ] SESSION_RECORD.md — Metadata and context
- [ ] INTENT.md — Phase 1 output
- [ ] DESIGN_SPEC.md — UI/UX specifications (if applicable)
- [ ] IMPLEMENTATION_LOG.md — Phase 2 log
- [ ] FIDELITY_REVIEW.md — Phase 3 review
- [ ] DEBATE_LOG.md — Internal disagreements (if any)

---

*Sessions are the unit of frontend work. No code changes occur outside sessions.*
