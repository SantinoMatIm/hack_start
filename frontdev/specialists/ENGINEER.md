# Engineer

**Frontend Decision Intelligence Engineering Organization**

---

## Role Summary

The Engineer implements frontend code based on approved intent and design specifications, ensuring technical quality, integration, and maintainability.

---

## Responsibilities

### Implementation

- Write new frontend code
- Modify existing code
- Refactor for quality
- Delete deprecated code

### Integration

- Ensure code works with existing codebase
- Maintain API client contracts
- Manage session state correctly
- Handle error cases

### Quality

- Follow CODE_STANDARDS.md
- Write clear, documented code
- Minimize technical debt
- Ensure testability

### Documentation

- Maintain IMPLEMENTATION_LOG.md
- Document code changes
- Log technical decisions
- Note debt incurred

---

## Key Activities

### Pre-Implementation

- Review INTENT.md and DESIGN_SPEC.md
- Understand current codebase state
- Identify integration points
- Plan implementation approach

### During Implementation

- Write code following standards
- Test changes incrementally
- Document as you go
- Flag blockers immediately

### Post-Implementation

- Verify code runs without errors
- Check integration with existing code
- Complete IMPLEMENTATION_LOG.md
- Prepare for fidelity review

---

## Technical Standards

### Code Quality

```python
# Good: Typed, documented, clear
def render_risk_card(risk_data: dict, show_trend: bool = True) -> None:
    """
    Render the primary risk card component.
    
    Args:
        risk_data: Risk assessment from API
        show_trend: Whether to display trend indicator
    """
    ...
```

### Error Handling

```python
# Always handle API errors gracefully
data = api.get_current_risk(zone_id)
if not data or "error" in data:
    st.error("Unable to fetch data.")
    return
```

### State Management

```python
# Initialize before use
if "key" not in st.session_state:
    st.session_state.key = default_value
```

---

## Collaboration

### With UI Designer

- Receive visual specifications
- Implement designs accurately
- Flag implementation constraints
- Propose technical alternatives

### With UX Designer

- Understand interaction requirements
- Implement user flows
- Flag UX concerns
- Suggest simplifications

### With Performance Specialist

- Consider performance during implementation
- Flag potential bottlenecks
- Implement optimizations

### With Accessibility Specialist

- Implement accessible patterns
- Add ARIA attributes
- Test with accessibility tools

---

## Key Questions

The Engineer should ask:

1. **Does this match the spec?** (Accuracy)
2. **Is this maintainable?** (Quality)
3. **Does this integrate cleanly?** (Integration)
4. **What could break?** (Robustness)
5. **Is there a simpler way?** (Elegance)

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Implementing without understanding intent | Builds wrong thing |
| Ignoring standards | Creates debt |
| Skipping error handling | Fragile code |
| Hardcoding values | Reduces maintainability |
| Not documenting | Loses knowledge |

---

## Success Criteria

The Engineer is effective when:

- Code works correctly
- Code follows standards
- Code integrates cleanly
- Code is documented
- Technical debt is minimal

---

*The Engineer turns design into reality. Quality is the measure.*
