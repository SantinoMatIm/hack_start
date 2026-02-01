# Escalation Policy

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines when and how to escalate issues that cannot be resolved within normal working session flow. Escalation is not failure — it is responsible recognition of boundaries.

---

## Escalation Philosophy

> **When in doubt, pause and ask. A delayed decision is better than a wrong one.**

The frontend serves high-stakes decision-making. Escalating uncertainty is better than shipping misleading interfaces.

---

## Escalation Triggers

### Immediate Escalation Required

| Trigger | Reason |
|---------|--------|
| Ambiguous requirements | Cannot determine what to build |
| Contradictory governance | Documents conflict with each other |
| Missing critical context | Cannot proceed without information |
| System behavior unexpected | Backend doesn't match documentation |
| Ethical concerns | Change could mislead users in harmful ways |
| Security concerns | Change could expose sensitive data |

### Escalation Recommended

| Trigger | Reason |
|---------|--------|
| Scope creep | Work expanding beyond session intent |
| Time-sensitive decisions | Need human input to meet deadline |
| Design trade-offs | Multiple valid approaches, need direction |
| Technical debt accumulation | Shortcuts becoming concerning |
| User impact uncertainty | Unsure how change affects decision-making |

### Self-Resolution First

| Situation | Try Before Escalating |
|-----------|----------------------|
| Minor ambiguity | Check governance docs, memory files |
| Technical question | Review existing code patterns |
| Design question | Check DESIGN_STANDARDS.md |
| Historical context | Review session history |

---

## Escalation Levels

### Level 1: Pause and Document

**For**: Minor blockers that may resolve with documentation

**Action**:
1. Pause current work
2. Document the issue in IMPLEMENTATION_LOG.md
3. List attempted resolutions
4. Continue with other work if possible
5. Return to issue later

**Example**: Unclear whether component should use variant A or B

### Level 2: Request Clarification

**For**: Blockers requiring human input

**Action**:
1. Use `/question` command during session
2. Clearly state the question
3. Provide context and options if applicable
4. Wait for response
5. Document resolution in session artifacts

**Example**: Intent says "improve urgency display" but doesn't specify which aspect

### Level 3: Formal Escalation

**For**: Significant blockers affecting session success

**Action**:
1. Document escalation in SESSION_RECORD.md
2. Create ESCALATION.md in session folder
3. Notify human of escalation status
4. Pause session or mark as blocked
5. Await resolution

**Example**: Discovered that API doesn't return data needed for intended change

### Level 4: Governance Escalation

**For**: Issues affecting organizational principles or structure

**Action**:
1. Document in session artifacts
2. Create proposal in councils/core-council/
3. Flag for governance review
4. Do not proceed until governance decision

**Example**: Proposed change would violate PRINCIPLES.md but seems necessary

---

## Escalation Format

### In-Session Question (`/question`)

```
/question [Your question here]

Context:
- [Relevant context]
- [What you've tried]
- [Why you need clarification]

Options (if applicable):
A. [Option A with trade-offs]
B. [Option B with trade-offs]
```

### ESCALATION.md Template

```markdown
# ESCALATION

## Session
{session-id}

## Escalation Level
Level [1/2/3/4]

## Issue Summary
[Brief description]

## Detailed Description
[Full context]

## Impact
- [What is blocked]
- [What can continue]

## Attempted Resolutions
1. [What you tried]
2. [What you tried]

## Options Identified
| Option | Pros | Cons |
|--------|------|------|
| A | | |
| B | | |

## Recommendation
[Your suggested path if you have one]

## Status
[ ] Awaiting response
[ ] In discussion
[ ] Resolved
[ ] Deferred

## Resolution
[Filled in when resolved]
```

---

## Escalation Response Times

| Level | Expected Response | Timeout Action |
|-------|-------------------|----------------|
| Level 1 | Self-resolution within session | Escalate to Level 2 |
| Level 2 | Human response within conversation | Document and continue where possible |
| Level 3 | May require conversation pause | Mark session as blocked |
| Level 4 | May span multiple sessions | Create governance ticket |

---

## Escalation Resolution

### When Resolution Received

1. Document resolution in escalation artifact
2. Update SESSION_RECORD.md
3. Resume work with new direction
4. Log lesson learned if applicable

### When Resolution Deferred

1. Document deferral reason
2. Identify workaround if possible
3. Create backlog item for future resolution
4. Continue with reduced scope if safe

### When Resolution Changes Direction

1. Update INTENT.md with new direction
2. May require re-approval of Gate 1
3. Document the pivot
4. Proceed with revised scope

---

## Common Escalation Scenarios

### Scenario: Unclear User Need

```
Trigger: "Improve the actions page" without specifics
Level: 2 (Request Clarification)
Question: "Which aspect of the actions page should be prioritized?
- Action card visual hierarchy
- Heuristic explanation clarity
- Selection UX for simulation
- Something else?"
```

### Scenario: Backend Mismatch

```
Trigger: API returns different structure than documented
Level: 3 (Formal Escalation)
Action: Document discrepancy, check if frontend or backend should change
```

### Scenario: Principle Tension

```
Trigger: "Urgency Is Visual" vs "Accessibility Is Non-Negotiable" conflict
Level: 2 or 4 depending on severity
Action: Request guidance on priority when animation conflicts with reduced motion
```

### Scenario: Scope Expansion

```
Trigger: During implementation, discovered related component needs update
Level: 1 or 2
Action: Document discovery, ask whether to expand scope or defer
```

---

## Escalation Don'ts

| Don't | Why |
|-------|-----|
| Escalate without trying self-resolution | Wastes time on solvable problems |
| Continue without escalating when blocked | Leads to wrong decisions |
| Escalate without clear question | Makes resolution harder |
| Escalate multiple issues at once without structure | Confuses the response |
| Assume escalation means failure | It means responsible recognition |

---

## Post-Escalation Learning

After significant escalations:

1. Add to memory/LESSONS_LEARNED.md
2. Identify if governance docs need update
3. Consider if similar situations will recur
4. Propose process improvements if warranted

---

*Escalation is a feature, not a bug. It protects decision-makers from misleading interfaces.*
