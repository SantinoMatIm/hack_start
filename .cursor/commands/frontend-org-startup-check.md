# Frontend Organization: Startup Check

Perform the startup protocol check without starting a full session.

## Instructions

You are the Frontend Lead performing startup validation.

**Execute the startup protocol checklist:**

Read and validate each required document exists and is coherent:

### Phase 1: Governance Documents
- [ ] `frontdev/README.md`
- [ ] `frontdev/PRINCIPLES.md`
- [ ] `frontdev/CONSTRAINTS.md`
- [ ] `frontdev/governance/STARTUP_PROTOCOL.md`
- [ ] `frontdev/governance/SESSION_PROTOCOL.md`
- [ ] `frontdev/governance/CODE_STANDARDS.md`
- [ ] `frontdev/governance/DESIGN_STANDARDS.md`
- [ ] `frontdev/governance/DECISION_FIDELITY.md`
- [ ] `frontdev/governance/APPROVAL_GATES.md`
- [ ] `frontdev/governance/ESCALATION_POLICY.md`

### Phase 2: Memory Documents
- [ ] `frontdev/memory/ARCHITECTURE_DECISIONS.md`
- [ ] `frontdev/memory/DESIGN_DECISIONS.md`
- [ ] `frontdev/memory/KNOWN_GAPS.md`
- [ ] `frontdev/memory/REVERSAL_LOG.md`
- [ ] `frontdev/memory/LESSONS_LEARNED.md`
- [ ] `frontdev/memory/USER_INSIGHTS.md`
- [ ] `frontdev/memory/backlog/surfaces.md`
- [ ] `frontdev/memory/backlog/technical_debt.md`
- [ ] `frontdev/memory/backlog/design_debt.md`
- [ ] `frontdev/memory/backlog/accessibility.md`

### Phase 3: Session Check
- [ ] List `frontdev/sessions/` for in-progress work

### Phase 4: Codebase Context
- [ ] `dashboard/app.py` exists
- [ ] `dashboard/pages/` has expected pages
- [ ] `dashboard/components/` has expected components

**Present results:**

```
═══════════════════════════════════════════════════════════════
   FRONTEND ORGANIZATION - STARTUP CHECK
═══════════════════════════════════════════════════════════════

GOVERNANCE DOCUMENTS: {✓ All present / ⚠️ Issues found}
{List any missing or problematic documents}

MEMORY DOCUMENTS: {✓ All present / ⚠️ Issues found}
{List any missing documents}

IN-PROGRESS SESSIONS: {count}
{List any sessions needing attention}

CODEBASE: {✓ Ready / ⚠️ Issues found}
{Any concerns about dashboard structure}

CONTRADICTIONS FOUND: {count}
{List any contradictions between documents}

OUTDATED CONTENT: {count}
{List any content that appears outdated}

═══════════════════════════════════════════════════════════════

STARTUP STATUS: {✓ READY / ⚠️ BLOCKED}

{If blocked, list what needs resolution}
{If ready, confirm organization can proceed with sessions}
═══════════════════════════════════════════════════════════════
```

This is a diagnostic check. It validates the organization is properly configured but doesn't start any work.
