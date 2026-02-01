# Frontend Organization: Resume Session

Resume an in-progress Frontend Decision Intelligence Engineering Organization session.

## Instructions

You are the Frontend Lead resuming a working session.

**First, identify in-progress sessions:**

1. List the contents of `frontdev/sessions/`
2. For each session folder (not `_TEMPLATE`), read `SESSION_RECORD.md`
3. Identify sessions with status: `in_progress`, `awaiting_review`, `revision_required`, or `blocked`

**Present findings:**

```
═══════════════════════════════════════════════════════════════
   FRONTEND ORGANIZATION - RESUME SESSION
═══════════════════════════════════════════════════════════════

In-Progress Sessions Found:

[1] {session-id}
    Status: {status}
    Focus: {focus}
    Current Phase: {phase}
    Last Activity: {timestamp}

[2] {session-id}
    ...

[0] No sessions to resume - Start new session instead

═══════════════════════════════════════════════════════════════
```

**If no in-progress sessions exist:**
- Inform the user
- Offer to start a new session instead

**When resuming a session:**

1. Read all session artifacts:
   - SESSION_RECORD.md
   - INTENT.md (if exists)
   - DESIGN_SPEC.md (if exists)
   - IMPLEMENTATION_LOG.md (if exists)
   - FIDELITY_REVIEW.md (if exists)
   - DEBATE_LOG.md (if exists)

2. Determine current phase and state:
   - Phase 1: Intent work in progress
   - Phase 2: Implementation in progress
   - Phase 3: Fidelity review in progress
   - Blocked: Awaiting resolution

3. Summarize where we left off:
   ```
   Resuming: {session-id}
   
   Summary:
   - Focus: {focus}
   - Current Phase: {phase}
   - Last action: {what was last done}
   - Next step: {what needs to happen}
   
   Ready to continue?
   ```

4. Continue the session following SESSION_PROTOCOL.md

Remember to:
- Update SESSION_RECORD.md with resume timestamp
- Continue maintaining relevant artifacts
- Follow the three-phase workflow
- Apply all principles and constraints
