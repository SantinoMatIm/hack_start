# Frontend Organization: Propose New Surface

Propose a new decision surface for the platform.

## Instructions

You are the Frontend Lead facilitating a surface proposal.

**Guide the user through proposing a new decision surface:**

```
═══════════════════════════════════════════════════════════════
   FRONTEND ORGANIZATION - PROPOSE NEW SURFACE
═══════════════════════════════════════════════════════════════

A "surface" is a distinct UI area that supports a specific
decision moment. Before proposing, consider:

• What decision does this surface enable?
• Who needs it (Government, Industry, or both)?
• What information must it display?
• What actions can users take from it?

═══════════════════════════════════════════════════════════════
```

**Gather information:**

1. **Decision Supported**: What decision does this enable?
2. **User Profile**: Government, Industry, or both?
3. **Description**: What would this surface do?
4. **Dependencies**: What must exist first?
5. **Estimated Complexity**: Low, Medium, or High?

**Validate against principles:**

Read `frontdev/PRINCIPLES.md` and check:
- Does this serve decision-making? (Decision Primacy)
- Is this actually needed? (No Dashboard Theater)
- Does it support the user profile? (Profile Differentiation)

**If valid, create the proposal:**

Add to `frontdev/memory/backlog/surfaces.md`:

```markdown
### SURFACE-{next-number}: {Name}

**Status**: Proposed
**Priority**: P{0-3}
**Related Gap**: {if applicable}

**Decision Supported**: {from user}
**User Profile**: {from user}
**Description**: {from user}
**Dependencies**: {from user}
**Estimated Complexity**: {from user}
```

**Present confirmation:**

```
═══════════════════════════════════════════════════════════════
   SURFACE PROPOSAL SUBMITTED
═══════════════════════════════════════════════════════════════

Surface: {name}
ID: SURFACE-{number}
Priority: P{n}

Added to: frontdev/memory/backlog/surfaces.md

Next steps:
• Design Council will review the proposal
• If approved, it can be scheduled for implementation
• Use "Start Session" and select option [2] to implement

═══════════════════════════════════════════════════════════════
```

**If not valid:**

Explain why the proposal doesn't align with principles and suggest alternatives or refinements.
