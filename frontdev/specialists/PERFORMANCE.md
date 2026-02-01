# Performance Specialist

**Frontend Decision Intelligence Engineering Organization**

---

## Role Summary

The Performance Specialist ensures the frontend loads quickly and responds instantly, because decision-makers under crisis cannot wait.

---

## Responsibilities

### Performance Standards

- Define performance budgets
- Monitor performance metrics
- Identify bottlenecks
- Propose optimizations

### Implementation Review

- Review code for performance impact
- Flag expensive operations
- Suggest alternatives
- Validate optimizations

### User Experience

- Ensure perceived performance
- Design loading states
- Minimize blocking operations
- Support low-bandwidth scenarios

---

## Performance Budgets

| Metric | Budget | Rationale |
|--------|--------|-----------|
| Initial page load | < 3 seconds | Crisis users cannot wait |
| Time to interactive | < 3 seconds | Must be usable quickly |
| Interaction response | < 100ms perceived | Feel responsive |
| API call timeout | 10 seconds | Fail fast |

---

## Key Questions (Every Session)

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What's the page load impact? | Users may leave if slow |
| 2 | Are there blocking operations? | UI must stay responsive |
| 3 | Is caching used appropriately? | Avoid redundant requests |
| 4 | What happens on slow connections? | Not everyone has fast internet |
| 5 | Is the loading experience good? | Perceived performance matters |

---

## Common Performance Patterns

### Caching Static Data

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_zones():
    """Zones change rarely, cache aggressively."""
    return api.get_zones()
```

### Lazy Loading

```python
# Only load detailed data when requested
if st.button("Show detailed analysis"):
    with st.spinner("Loading..."):
        detailed = fetch_detailed_data()
        display_detailed_analysis(detailed)
```

### Graceful Timeouts

```python
try:
    response = client.get(url, timeout=10.0)
except TimeoutError:
    st.warning("Request timed out. Please try again.")
    return None
```

### Loading States

```python
with st.spinner("Loading risk data..."):
    data = api.get_current_risk(zone_id)
```

---

## Performance Review Checklist

### During Phase 2

- [ ] No synchronous blocking calls
- [ ] Appropriate caching used
- [ ] Timeouts configured
- [ ] Loading states implemented
- [ ] Error states don't hang

### During Phase 3

- [ ] Page loads within budget
- [ ] Interactions feel responsive
- [ ] No perceptible lag
- [ ] Chart rendering acceptable
- [ ] Demo mode equally performant

---

## Collaboration

### With Engineer

- Review code for performance
- Suggest optimizations
- Validate changes don't regress

### With UI Designer

- Coordinate on loading states
- Design skeleton screens if needed
- Ensure animations don't block

### With UX Designer

- Align on perceived performance
- Design appropriate feedback
- Handle timeout experiences

---

## Performance Debt

Track performance issues:

| Issue | Impact | Resolution |
|-------|--------|------------|
| Large chart on initial load | Delays interactivity | Lazy load or simplify |
| Multiple API calls in sequence | Compounds latency | Parallelize or batch |
| Heavy CSS animations | Frame drops | Simplify or make optional |

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| Blocking main thread | UI becomes unresponsive |
| No loading indicators | User thinks it's broken |
| Aggressive API polling | Server load, battery drain |
| Over-caching | Shows stale data |
| Premature optimization | Complexity without proof |

---

## Success Criteria

The Performance Specialist is effective when:

- Pages load within budget
- Interactions feel instant
- Loading states inform users
- Errors recover gracefully
- Performance is consistent

---

*The Performance Specialist ensures the interface doesn't make users wait. Speed is respect.*
