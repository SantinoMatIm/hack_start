# Startup Protocol

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This protocol defines the mandatory startup phase that must complete before any frontend code is written, modified, or deleted. It exists to ensure the organization absorbs context, intent, constraints, and institutional memory before acting.

---

## Protocol Status

This is a **blocking protocol**. No frontend work may proceed until startup is complete.

---

## Startup Checklist

### Phase 1: Governance Absorption

- [ ] Read `frontdev/README.md` — Organization charter
- [ ] Read `frontdev/PRINCIPLES.md` — Core principles
- [ ] Read `frontdev/CONSTRAINTS.md` — Technical and governance boundaries
- [ ] Read `frontdev/governance/SESSION_PROTOCOL.md` — Working session procedures
- [ ] Read `frontdev/governance/CODE_STANDARDS.md` — Code quality expectations
- [ ] Read `frontdev/governance/DESIGN_STANDARDS.md` — Visual and interaction standards
- [ ] Read `frontdev/governance/DECISION_FIDELITY.md` — Truth constraints
- [ ] Read `frontdev/governance/APPROVAL_GATES.md` — Phase approval criteria
- [ ] Read `frontdev/governance/ESCALATION_POLICY.md` — When to pause and escalate

### Phase 2: Memory Review

- [ ] Read `frontdev/memory/ARCHITECTURE_DECISIONS.md` — Past architectural choices
- [ ] Read `frontdev/memory/DESIGN_DECISIONS.md` — Past design choices
- [ ] Read `frontdev/memory/KNOWN_GAPS.md` — Documented missing surfaces
- [ ] Read `frontdev/memory/REVERSAL_LOG.md` — Decisions that were reversed
- [ ] Read `frontdev/memory/LESSONS_LEARNED.md` — Cross-session learnings
- [ ] Read `frontdev/memory/USER_INSIGHTS.md` — UX research findings
- [ ] Scan `frontdev/memory/backlog/` — Pending work items

### Phase 3: Session Continuity

- [ ] List all folders in `frontdev/sessions/`
- [ ] Identify any sessions with `status: in_progress`
- [ ] For in-progress sessions:
  - [ ] Read SESSION_RECORD.md
  - [ ] Read most recent artifacts
  - [ ] Determine current phase and blockers
- [ ] Decide: Resume existing session or start new?

### Phase 4: Codebase Context

- [ ] Review `dashboard/app.py` — Current main entry
- [ ] Scan `dashboard/pages/` — Existing pages
- [ ] Scan `dashboard/components/` — Existing components
- [ ] Review `dashboard/assets/styles.css` — Design system state

### Phase 5: Validation

- [ ] Surface any contradictions between governance documents
- [ ] Surface any outdated assumptions in memory
- [ ] Surface any conflicts between current code and documented decisions
- [ ] Log all surfaced issues

---

## Startup Outcomes

### On Successful Startup

If all checks pass and no blockers exist:

```
STARTUP COMPLETE
================
- Governance: Absorbed
- Memory: Reviewed
- Sessions: No in-progress work (or: Resuming session {id})
- Codebase: Context established
- Issues: None (or: {n} issues logged for discussion)

Ready to proceed with:
[ ] New session
[ ] Resume session {id}
[ ] Address logged issues first
```

### On Blocked Startup

If critical issues are found:

```
STARTUP BLOCKED
===============
Reason: {description}

Required resolution:
1. {action needed}
2. {action needed}

Cannot proceed until resolved.
```

---

## Common Blocking Conditions

| Condition | Resolution |
|-----------|------------|
| Contradictory governance documents | Escalate to Core Council |
| Incomplete in-progress session with unclear state | Request human clarification |
| Code and documentation out of sync | Document discrepancy, propose alignment |
| Missing critical memory (e.g., no ARCHITECTURE_DECISIONS.md) | Create initial document or request context |
| Ambiguous user intent | Request clarification before proceeding |

---

## Startup Artifacts

If startup surfaces significant issues, create:

```
frontdev/sessions/{date}-startup-review/
├── SESSION_RECORD.md
├── ISSUES_FOUND.md
└── RESOLUTION_PLAN.md
```

This treats startup review as its own mini-session when warranted.

---

## Startup Timing

| Trigger | Startup Required? |
|---------|-------------------|
| First interaction in new conversation | Yes, full startup |
| Continuing from previous message | No, if context maintained |
| Human says "start over" or "fresh start" | Yes, full startup |
| Switching to different work area | Partial startup (relevant memory) |
| After governance document changes | Yes, re-absorb governance |

---

## Startup Ritual Mindset

Treat this startup phase as you would:
- An internal onboarding for a new team member
- A technical kickoff meeting before a sprint
- A production handoff briefing

It is not bureaucracy. It is context establishment that prevents:
- Repeated mistakes
- Contradictory decisions
- Lost institutional knowledge
- Drift from principles

---

*Startup is not optional. It is the foundation of coherent frontend work.*
