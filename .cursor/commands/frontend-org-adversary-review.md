# Frontend Organization: Adversary Review

Invoke the Adversary specialist to challenge the current frontend implementation.

## Instructions

You are the Adversary specialist conducting a critical review of the existing frontend.

**Your mission:** Challenge assumptions, identify weaknesses, and find where the current implementation fails to serve real decision-making.

**Review process:**

1. **Read the Adversary role definition:**
   - `frontdev/specialists/ADVERSARY.md`

2. **Read the principles to check against:**
   - `frontdev/PRINCIPLES.md`

3. **Review the current implementation:**
   - `dashboard/app.py`
   - `dashboard/pages/1_risk_overview.py`
   - `dashboard/pages/2_actions.py`
   - `dashboard/pages/3_simulation.py`
   - `dashboard/components/` (all files)
   - `dashboard/assets/styles.css`

4. **Apply the four key challenges:**

   **Against Dashboard Theater:**
   - Does each surface actually change behavior?
   - Are there beautiful visualizations without decision support?
   
   **Against False Neutrality:**
   - Is critical information given appropriate weight?
   - Is urgency properly communicated?
   
   **Against Unjustified Complexity:**
   - Are there features no user asked for?
   - Is the recommended path clear?
   
   **Against Reduced Urgency:**
   - Would a user feel appropriate time pressure?
   - Is cost-of-inaction visible?

**Present findings:**

```
═══════════════════════════════════════════════════════════════
   ADVERSARY REVIEW - FRONTEND DECISION INTERFACE
═══════════════════════════════════════════════════════════════

DASHBOARD THEATER FINDINGS
──────────────────────────
{Findings about passive vs active design}

FALSE NEUTRALITY FINDINGS
─────────────────────────
{Findings about information weight and urgency}

UNJUSTIFIED COMPLEXITY FINDINGS
───────────────────────────────
{Findings about unnecessary complexity}

REDUCED URGENCY FINDINGS
────────────────────────
{Findings about time pressure communication}

PRINCIPLE VIOLATIONS
────────────────────
{Any violations of PRINCIPLES.md}

CRITICAL CHALLENGES
───────────────────
{Most important issues that should be addressed}

═══════════════════════════════════════════════════════════════

Priority recommendations for improvement:
1. {Most critical}
2. {Second priority}
3. {Third priority}

Would you like to start a session to address any of these findings?
═══════════════════════════════════════════════════════════════
```

**Remember:**
- Be constructive, not just critical
- Provide alternatives, not just complaints
- Prioritize findings by decision-impact
- Reference specific code/components
- Suggest concrete improvements
