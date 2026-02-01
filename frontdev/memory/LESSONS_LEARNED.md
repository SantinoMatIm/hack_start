# Lessons Learned

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document captures cross-session learnings that improve future work. Lessons emerge from successful sessions, failures, reversals, and retrospectives.

---

## Lesson Format

```
## LL-{number}: {Title}

**Source**: [Session ID, Reversal ID, or observation]
**Date**: YYYY-MM-DD
**Category**: Process | Technical | Design | Collaboration

**Situation**: [What happened]
**Learning**: [What we learned]
**Application**: [How to apply this going forward]
```

---

## Lessons

### LL-001: Start with User Profiles, Not Features

**Source**: Organization founding
**Date**: 2026-01-31
**Category**: Design

**Situation**:
When designing frontend surfaces, the temptation is to start with "what features should this have?"

**Learning**:
Starting with user profiles (Government vs Industry) and their decision contexts leads to better outcomes. Different profiles have different mental models, priorities, and accountability requirements.

**Application**:
- Every session INTENT.md must specify target user profile
- Design specs must include profile-specific considerations
- Validate features against profile needs, not abstract usefulness

---

### LL-002: Uncertainty is Information, Not Noise

**Source**: PRINCIPLES.md development
**Date**: 2026-01-31
**Category**: Design

**Situation**:
Initial instinct is to show clean, precise numbers to appear professional and confident.

**Learning**:
For decision-support interfaces, hiding uncertainty reduces trust and defensibility. Users making high-stakes decisions need to know what's estimated vs certain.

**Application**:
- Always label projections as projections
- Show confidence levels where available
- "Estimated" and "measured" should be visually distinct
- This is not lack of polish; it is fidelity

---

### LL-003: Visual Urgency Requires Multiple Dimensions

**Source**: Gap identification (GAP-001)
**Date**: 2026-01-31
**Category**: Design

**Situation**:
Color-coding risk levels (red/orange/yellow/green) was assumed sufficient for urgency communication.

**Learning**:
Color alone is not enough for urgency communication. Users may be color-blind, working in difficult lighting, or habituated to color codes. True urgency requires size, weight, position, and potentially motion.

**Application**:
- Use color + size + weight for urgency
- Consider animation for critical states (with reduced-motion fallback)
- Never rely on color alone (accessibility requirement)

---

### LL-004: "Dashboard" is an Anti-Pattern Word

**Source**: PRINCIPLES.md development
**Date**: 2026-01-31
**Category**: Process

**Situation**:
Team members may default to "dashboard" thinking when designing interfaces.

**Learning**:
The word "dashboard" connotes passive display. Decision interfaces compel action. Using "dashboard" in discussion biases toward passive design.

**Application**:
- Prefer "decision surface" or "decision interface"
- When someone says "dashboard," ask "what decision does this enable?"
- Challenge designs that display without compelling

---

### LL-005: Adversary Role Improves Quality

**Source**: Organization design
**Date**: 2026-01-31
**Category**: Process

**Situation**:
Designing with only constructive feedback leads to blind spots.

**Learning**:
Explicit devil's advocate (Adversary) role surfaces problems before they reach production. Easy consensus is a warning sign.

**Application**:
- Invoke Adversary review at Phase 1 (challenge intent)
- Use /adversary command when design feels "too easy"
- Log adversary challenges even when not adopted

---

### LL-006: Session Artifacts Enable Recovery

**Source**: SESSION_PROTOCOL.md development
**Date**: 2026-01-31
**Category**: Process

**Situation**:
Work done without documentation is work that cannot be understood, continued, or learned from.

**Learning**:
Session artifacts (INTENT.md, IMPLEMENTATION_LOG.md, etc.) are not bureaucracy — they are recovery mechanisms. When sessions span multiple conversations, artifacts enable continuation.

**Application**:
- Never skip artifact creation
- Write artifacts as you go, not at the end
- Artifacts should stand alone (someone else could read and understand)

---

### LL-007: Escalation is a Feature

**Source**: ESCALATION_POLICY.md development
**Date**: 2026-01-31
**Category**: Collaboration

**Situation**:
There's natural reluctance to escalate issues (feels like admitting failure).

**Learning**:
In high-stakes decision support, shipping something wrong is worse than pausing to clarify. Escalation protects users from misleading interfaces.

**Application**:
- Normalize escalation as responsible behavior
- "I don't know" is a valid answer that triggers escalation
- Praise escalations that prevent problems

---

## Lessons by Category

### Process
- LL-004: "Dashboard" is an Anti-Pattern Word
- LL-005: Adversary Role Improves Quality
- LL-006: Session Artifacts Enable Recovery

### Design
- LL-001: Start with User Profiles, Not Features
- LL-002: Uncertainty is Information, Not Noise
- LL-003: Visual Urgency Requires Multiple Dimensions

### Technical
*No technical lessons recorded yet.*

### Collaboration
- LL-007: Escalation is a Feature

---

## How to Add a Lesson

1. Assign next sequential number
2. Document source (where learning came from)
3. Write clearly for future readers
4. Categorize appropriately
5. Update category index above

---

## Lesson Review

Lessons should be reviewed:
- At the start of each session (part of startup)
- When similar situations arise
- Periodically for pattern identification

---

*Lessons compound. Each one makes future work better.*
