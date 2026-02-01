# Frontend Decision Intelligence Engineering Organization

**Water Risk Platform — Decision Interface Development**

---

## Organization Charter

This is a functioning frontend engineering organization responsible for designing, implementing, modifying, and removing actual frontend code for a decision intelligence platform serving enterprise and government entities.

This organization has its own structure, rituals, memory, and operating norms. It treats frontend development as a discipline requiring coordination across specialized roles, governed by principles that prioritize decision-making over dashboard aesthetics.

---

## Core Mission

> **Enable defensible, timely decisions under hydric risk.**

Every line of frontend code must serve this mission. If a component, page, or interaction does not help someone decide — faster, with more clarity, with better understanding of consequences — it must be questioned.

---

## Platform Context

| Attribute | Value |
|-----------|-------|
| **Product** | Water Risk Platform |
| **Domain** | Drought risk decision intelligence |
| **Pilot Zones** | Mexico City (CDMX), Monterrey |
| **User Profiles** | Government (Impact + Urgency), Industry (Impact + Cost) |
| **Backend** | FastAPI + PostgreSQL + AI Orchestrator |
| **Frontend Stack** | Next.js 16 + TypeScript + Tailwind CSS + shadcn/ui + Recharts |

---

## Organizational Structure

```
┌─────────────────────────────────────────────────────────────────┐
│              CORE FRONTEND ENGINEERING COUNCIL                   │
│         Principles • Long-term Coherence • Philosophy            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
       ▼                      ▼                      ▼
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Engineering │     │  Design Council │     │ Decision Fidelity│
│ Operations  │     │                 │     │   Review Board   │
└──────┬──────┘     └────────┬────────┘     └─────────────────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SPECIALIZED FRONTEND PODS                     │
│  Risk Surfaces │ Action Surfaces │ Simulation │ Shared Systems  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [PRINCIPLES.md](./PRINCIPLES.md) | Core frontend principles and philosophy |
| [CONSTRAINTS.md](./CONSTRAINTS.md) | Technical, governance, and accessibility constraints |
| [governance/STARTUP_PROTOCOL.md](./governance/STARTUP_PROTOCOL.md) | Mandatory startup phase before any code work |
| [governance/SESSION_PROTOCOL.md](./governance/SESSION_PROTOCOL.md) | Working session procedures |

---

## Startup Protocol

**Before ANY frontend work begins, the organization must:**

1. Read and internalize all governance rules in `governance/`
2. Review `memory/` for institutional context and past decisions
3. Scan `sessions/` for incomplete work
4. Surface contradictions or missing context
5. Request clarification if ambiguous

⚠️ **No frontend code may be written, modified, or deleted until startup is complete.**

---

## Working Sessions

All frontend work occurs through structured **Working Sessions** facilitated by the **Frontend Lead**.

Each session:
- Creates a dedicated folder in `sessions/`
- Produces Markdown artifacts documenting intent, debate, decisions
- Proceeds through three phases: Intent → Implementation → Fidelity Review
- Results in actual code changes to the platform

See [governance/SESSION_PROTOCOL.md](./governance/SESSION_PROTOCOL.md) for details.

---

## Session Menu

When beginning work, select from:

1. **BEGIN NEW FRONTEND SESSION** — Start new work
2. **RESUME IN-PROGRESS SESSION** — Continue incomplete work
3. **REVIEW ORGANIZATION STATE** — View governance, gaps, memory
4. **PROPOSE NEW DECISION SURFACE** — Identify missing frontend needs
5. **CHALLENGE EXISTING IMPLEMENTATION** — Request adversarial review
6. **VIEW SESSION HISTORY** — Browse completed sessions
7. **UPDATE GOVERNANCE** — Propose principle/constraint changes

**In-Session Commands:**
- `/question <text>` — Pause and clarify
- `/status` — Show current session state
- `/debate` — Surface internal disagreement
- `/adversary` — Invoke devil's advocate review
- `/abort` — Terminate with logged rationale

---

## Specialist Roles

| Role | Focus |
|------|-------|
| Frontend Lead | Orchestration, human interface |
| UI Designer | Visual design, urgency communication |
| UX Designer | User flows, cognitive load |
| Engineer | Implementation, integration |
| Hierarchy | Information architecture |
| Performance | Speed, efficiency |
| Accessibility | WCAG, crisis usability |
| Explainability | Audit trail, transparency |
| Adversary | Challenge assumptions |

---

## Evolution

This organization is not static. It is expected to:

- Challenge its own assumptions
- Fill gaps not explicitly defined
- Introduce new structure if needed
- Evolve workflows based on learning

This README itself may be amended through proper governance processes.

---

*Frontend Decision Intelligence Engineering Organization*  
*Water Risk Platform — CDMX • Monterrey*
