# Frontend Organization: Quick Gap Session

Quickly start a session focused on one of the known gaps.

## Instructions

You are the Frontend Lead starting a focused session on a documented gap.

**First, read the known gaps:**
- `frontdev/memory/KNOWN_GAPS.md`

**Present the gaps for selection:**

```
═══════════════════════════════════════════════════════════════
   FRONTEND ORGANIZATION - ADDRESS A GAP
═══════════════════════════════════════════════════════════════

Select a gap to address:

[1] GAP-001: Urgency Visual Escalation (Major)
    Days-to-critical needs progressive visual treatment

[2] GAP-002: Cost of Inaction Visibility (Major)
    Show what users lose by waiting

[3] GAP-003: Decision Audit Trail (Major)
    Persistent log of decisions for accountability

[4] GAP-004: Uncertainty Visualization (Major)
    Confidence intervals and ranges on projections

[5] GAP-005: Multi-Zone Comparison (Minor)
    Side-by-side zone comparison for resource allocation

[6] GAP-006: Escalation Threshold Visibility (Minor)
    Show distance to next risk level

═══════════════════════════════════════════════════════════════
```

**Once selected:**

1. Create session folder: `frontdev/sessions/{date}-gap-{number}-{slug}/`

2. Copy templates from `_TEMPLATE/`

3. Pre-populate INTENT.md with:
   - Gap description from KNOWN_GAPS.md
   - Current state analysis
   - Hypotheses about improvement

4. Begin Phase 1 quickly:
   - Review the specific area of code affected
   - Confirm the gap analysis
   - Propose specific changes
   - Seek human approval

5. Proceed through phases:
   - Phase 2: Implement the fix
   - Phase 3: Verify fidelity

**This is a streamlined flow for documented gaps.** The gap analysis is already done; focus on solution and implementation.

Remember to:
- Update KNOWN_GAPS.md status to "In Progress"
- Follow all principles and constraints
- Update gap status to "Resolved" when complete
