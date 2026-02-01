# User Insights

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document captures user research findings, behavioral observations, and user feedback that inform frontend design decisions. The UX Designer role owns this document.

---

## User Profiles

### Government Profile

**Description**: Public officials managing drought response for metropolitan areas

| Attribute | Detail |
|-----------|--------|
| **Primary Goal** | Protect public welfare through effective water management |
| **Decision Mode** | Accountable to citizens; needs defensible rationale |
| **Priorities** | Impact + Urgency (public welfare first) |
| **Key Anxiety** | Political fallout from poor decisions or slow response |
| **Information Need** | Clear audit trail, justification for each action |
| **Time Pressure** | High during crises; moderate during monitoring |

**Behavioral Observations**:
- Need to explain decisions to non-technical stakeholders
- Value documentation and audit trails
- May have multiple zones under responsibility
- Often working in crisis conditions with degraded attention
- May need to present information to media or public

**Design Implications**:
- Provide clear justification text for all recommendations
- Make audit trail visible and exportable
- Support multi-zone management
- Design for stress: clear hierarchy, minimal cognitive load
- Include public-facing summary potential

---

### Industry Profile

**Description**: Operations managers ensuring business continuity under water risk

| Attribute | Detail |
|-----------|--------|
| **Primary Goal** | Maintain operational continuity with acceptable cost |
| **Decision Mode** | ROI-focused; board accountability |
| **Priorities** | Impact + Cost (efficiency first) |
| **Key Anxiety** | Operational disruption, financial exposure |
| **Information Need** | Cost-benefit clarity, implementation feasibility |
| **Time Pressure** | Moderate; focus on planning horizon |

**Behavioral Observations**:
- Need to justify expenditure to leadership
- Value quantified impact metrics
- May have single facility or regional responsibility
- Focus on operational impact over public messaging
- Need implementation-ready recommendations

**Design Implications**:
- Include cost metrics where available
- Show ROI or cost-benefit indicators
- Provide implementation guidance
- Focus on operational language over civic language
- Support planning horizon visualization

---

## Research Findings

### RF-001: Crisis Cognition Degradation

**Source**: General UX research on crisis interfaces
**Date**: 2026-01-31
**Confidence**: High (established research)

**Finding**:
Users under stress experience:
- Reduced attention span
- Narrowed focus (tunnel vision)
- Impaired fine motor control
- Decreased working memory
- Faster decision-making (sometimes too fast)

**Implication**:
- Design for degraded user state
- Reduce choices to essentials
- Make primary action extremely clear
- Use larger touch targets
- Avoid complex multi-step flows during crisis

---

### RF-002: Decision Makers Need Defensibility

**Source**: Stakeholder interviews (conceptual)
**Date**: 2026-01-31
**Confidence**: Medium (informed assumption)

**Finding**:
Both government and industry users need to defend decisions to others (citizens, boards, media). They need to answer "Why did you decide this?"

**Implication**:
- Every recommendation needs visible justification
- Decision trail must be recordable
- Methodology must be accessible
- Numbers must be traceable to source

---

### RF-003: Consequence Visibility Drives Action

**Source**: Behavioral economics research
**Date**: 2026-01-31
**Confidence**: High (established research)

**Finding**:
People are more motivated by loss aversion than gain seeking. "What you will lose" is more compelling than "what you will gain."

**Implication**:
- Show cost of inaction prominently
- Frame as "days lost" not just "days gained"
- Make consequence comparison visual
- "Without action..." should be as prominent as "With action..."

---

### RF-004: Uncertainty Tolerance Varies

**Source**: General research on expert vs novice users
**Date**: 2026-01-31
**Confidence**: Medium

**Finding**:
Expert users (technical, domain-familiar) tolerate and even expect uncertainty communication. Novice users may find uncertainty confusing or anxiety-inducing.

**Implication**:
- Consider user expertise level
- Provide progressive disclosure of uncertainty details
- Make methodology accessible but not mandatory
- Default to honest uncertainty; allow deeper exploration

---

## Feedback Log

### Format

```
## FB-{number}: {Summary}

**Date**: YYYY-MM-DD
**Source**: [User type, context]
**Feedback**: [What was said/observed]
**Action**: [Taken | Backlog | Deferred | Rejected]
**Notes**: [Additional context]
```

### Feedback Entries

*No direct user feedback recorded yet. This section will be populated as user testing occurs.*

---

## Usability Observations

### UO-001: Zone Selection Clarity

**Date**: 2026-01-31
**Source**: Interface review
**Observation**: Zone selection on landing page uses buttons that look similar. Selected vs unselected state could be more distinct.
**Status**: Noted for future session

---

### UO-002: Action Selection Friction

**Date**: 2026-01-31
**Source**: Interface review
**Observation**: Selecting actions for simulation requires scrolling through cards and using small checkboxes. May be friction under stress.
**Status**: Noted for future session (GAP candidate)

---

## Personas (Detailed)

### Persona: Maria — Government Water Authority Director

**Demographics**:
- Age: 52
- Role: Director of Water Resources, Mexico City
- Experience: 20 years in public service

**Context**:
- Manages water policy for 21 million people
- Reports to mayor's office
- Frequently speaks to media
- Works with multiple departments

**Goals**:
- Prevent water crisis
- Make defensible decisions
- Coordinate across agencies
- Communicate clearly to public

**Frustrations**:
- Data scattered across systems
- Decisions questioned without clear trail
- Crisis situations are chaotic
- Political pressure to act vs wait

**Quote**: "I need to explain to the mayor why we're implementing restrictions. Give me the numbers that justify this."

---

### Persona: Roberto — Industrial Operations Manager

**Demographics**:
- Age: 41
- Role: Operations Manager, Manufacturing Plant
- Experience: 15 years in industrial operations

**Context**:
- Manages facility in Monterrey
- Reports to regional VP
- Responsible for production continuity
- Water is critical to operations

**Goals**:
- Maintain production levels
- Minimize operational costs
- Plan for contingencies
- Meet regulatory requirements

**Frustrations**:
- Unclear lead time for restrictions
- Difficulty planning capital expenditure
- Reactive rather than proactive information
- Compliance reporting burden

**Quote**: "Tell me what's coming and what it will cost us. I need to plan."

---

## How to Update

1. Add research findings with confidence level
2. Log user feedback when received
3. Update personas as understanding deepens
4. Reference insights in DESIGN_SPEC.md during sessions

---

*User insights ground design in reality. Without them, we design for imagined users.*
