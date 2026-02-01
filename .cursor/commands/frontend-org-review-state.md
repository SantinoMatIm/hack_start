# Frontend Organization: Review State

Review the current state of the Frontend Decision Intelligence Engineering Organization.

## Instructions

You are the Frontend Lead providing an organization state review.

**Gather and present the following information:**

1. **Read backlogs and memory:**
   - `frontdev/memory/KNOWN_GAPS.md`
   - `frontdev/memory/backlog/surfaces.md`
   - `frontdev/memory/backlog/technical_debt.md`
   - `frontdev/memory/backlog/design_debt.md`
   - `frontdev/memory/backlog/accessibility.md`
   - `frontdev/memory/LESSONS_LEARNED.md`

2. **Check session status:**
   - List `frontdev/sessions/` for completed and in-progress sessions

3. **Review decisions:**
   - `frontdev/councils/core-council/DECISIONS.md`
   - `frontdev/memory/ARCHITECTURE_DECISIONS.md`
   - `frontdev/memory/DESIGN_DECISIONS.md`

**Present the state report:**

```
═══════════════════════════════════════════════════════════════
   FRONTEND ORGANIZATION - STATE REPORT
═══════════════════════════════════════════════════════════════

KNOWN GAPS ({count})
────────────────────
{List gaps with severity}

SURFACES BACKLOG ({count})
─────────────────────────
{List proposed surfaces with priority}

TECHNICAL DEBT ({count})
────────────────────────
{List debt items with severity}

DESIGN DEBT ({count})
─────────────────────
{List design debt items}

ACCESSIBILITY ISSUES ({count})
──────────────────────────────
{List a11y issues with severity}

SESSIONS
────────
Completed: {count}
In Progress: {count}
{List any in-progress sessions}

RECENT DECISIONS
────────────────
{List recent council/architecture/design decisions}

LESSONS LEARNED
───────────────
{Count and notable patterns}

═══════════════════════════════════════════════════════════════

Recommendations:
1. {Priority recommendation based on gaps/debt}
2. {Secondary recommendation}

Would you like to:
[1] Start a session to address a specific item
[2] Deep dive into a particular area
[3] Update any of this information
═══════════════════════════════════════════════════════════════
```

This is a read-only review. If the user wants to take action, guide them to start or resume a session.
