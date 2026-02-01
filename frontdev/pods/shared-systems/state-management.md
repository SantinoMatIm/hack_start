# State Management Patterns

**Shared Systems Pod — Frontend Decision Intelligence Engineering Organization**

---

## Overview

This document defines patterns for managing state in the Next.js frontend.

---

## State Categories

| Category | Tool | Persistence | Use Case |
|----------|------|-------------|----------|
| Component State | `useState` | None | UI toggles, form inputs, loading states |
| Derived State | `useMemo` | None | Computed values from props/state |
| Cross-Page State | `localStorage` | Browser | Selected actions, zone preference |
| Shareable State | URL params | None | Links that preserve context |

---

## Component State

### Basic Pattern

```typescript
'use client';

import { useState } from 'react';

export function ActionSelector() {
  const [selectedActions, setSelectedActions] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  
  const toggleAction = (code: string) => {
    setSelectedActions(prev => {
      const next = new Set(prev);
      if (next.has(code)) {
        next.delete(code);
      } else {
        next.add(code);
      }
      return next;
    });
  };
  
  return (
    // ...
  );
}
```

### Multiple Related States

```typescript
interface PageState {
  data: RiskResponse | null;
  loading: boolean;
  error: string | null;
}

// Group related states
const [risk, setRisk] = useState<RiskResponse | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

---

## Cross-Page State (localStorage)

### Saving State

```typescript
// Save selected actions for simulation page
const proceedToSimulation = () => {
  localStorage.setItem('selectedActions', JSON.stringify(Array.from(selectedActions)));
  localStorage.setItem('selectedZone', selectedZone);
  router.push('/simulation');
};
```

### Loading State

```typescript
useEffect(() => {
  // Load from localStorage on mount
  const storedActions = localStorage.getItem('selectedActions');
  const storedZone = localStorage.getItem('selectedZone');
  
  if (storedActions) {
    setSelectedActions(new Set(JSON.parse(storedActions)));
  }
  if (storedZone) {
    setSelectedZone(storedZone);
  }
}, []);
```

### Clearing State

```typescript
const resetSelection = () => {
  localStorage.removeItem('selectedActions');
  setSelectedActions(new Set());
};
```

---

## URL State (Shareable)

### Reading URL Params

```typescript
'use client';

import { useSearchParams } from 'next/navigation';

export default function RiskPage() {
  const searchParams = useSearchParams();
  const zone = searchParams.get('zone') || 'cdmx';
  const profile = searchParams.get('profile') || 'government';
  
  // Use zone and profile...
}
```

### Updating URL

```typescript
import { useRouter, useSearchParams } from 'next/navigation';

export function ZoneSelector() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const updateZone = (zone: string) => {
    const params = new URLSearchParams(searchParams);
    params.set('zone', zone);
    router.push(`?${params.toString()}`);
  };
  
  return (
    // ...
  );
}
```

---

## Derived State (useMemo)

### Computing Values

```typescript
import { useMemo } from 'react';

export function ActionSummary({ actions, selectedCodes }: Props) {
  // Memoize expensive computation
  const totalDaysGained = useMemo(() => {
    return actions
      .filter(a => selectedCodes.has(a.action_code))
      .reduce((sum, a) => sum + a.expected_effect.days_gained, 0);
  }, [actions, selectedCodes]);
  
  const selectedActions = useMemo(() => {
    return actions.filter(a => selectedCodes.has(a.action_code));
  }, [actions, selectedCodes]);
  
  return (
    <div>
      <p>{selectedActions.length} actions selected</p>
      <p>+{totalDaysGained} days gained</p>
    </div>
  );
}
```

---

## Callback Memoization (useCallback)

### Event Handlers Passed as Props

```typescript
import { useCallback } from 'react';

export function ActionsPage() {
  const [selectedActions, setSelectedActions] = useState<Set<string>>(new Set());
  
  // Memoize to prevent unnecessary re-renders
  const handleToggle = useCallback((code: string) => {
    setSelectedActions(prev => {
      const next = new Set(prev);
      if (next.has(code)) {
        next.delete(code);
      } else {
        next.add(code);
      }
      return next;
    });
  }, []);
  
  return (
    <div>
      {actions.map(action => (
        <ActionCard
          key={action.action_code}
          action={action}
          selected={selectedActions.has(action.action_code)}
          onToggle={handleToggle}
        />
      ))}
    </div>
  );
}
```

---

## Data Fetching State

### Standard Pattern

```typescript
export function useRiskData(zoneId: string) {
  const [data, setData] = useState<RiskResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    let cancelled = false;
    
    async function fetchData() {
      setLoading(true);
      setError(null);
      
      try {
        const result = await api.getCurrentRisk(zoneId);
        if (!cancelled) {
          setData(result);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Failed to fetch');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }
    
    fetchData();
    
    // Cleanup to prevent state updates on unmounted component
    return () => {
      cancelled = true;
    };
  }, [zoneId]);
  
  return { data, loading, error };
}
```

---

## State Patterns by Page

### Risk Overview

```typescript
// State needed
const [selectedZone, setSelectedZone] = useState('cdmx');
const [risk, setRisk] = useState<RiskResponse | null>(null);
const [history, setHistory] = useState<RiskHistoryResponse | null>(null);
const [loading, setLoading] = useState(true);
const [isDemo, setIsDemo] = useState(false);
```

### Actions Page

```typescript
// State needed
const [selectedZone, setSelectedZone] = useState('cdmx');
const [selectedProfile, setSelectedProfile] = useState<Profile>('government');
const [recommendations, setRecommendations] = useState<RecommendedActionsResponse | null>(null);
const [selectedActions, setSelectedActions] = useState<Set<string>>(new Set());
const [loading, setLoading] = useState(false);
```

### Simulation Page

```typescript
// State needed (loaded from localStorage)
const [selectedActions, setSelectedActions] = useState<string[]>([]);
const [selectedZone, setSelectedZone] = useState('cdmx');
const [simulation, setSimulation] = useState<SimulationResponse | null>(null);
const [loading, setLoading] = useState(false);
```

---

## Future Considerations

If state management becomes more complex, consider:

1. **Zustand** - Lightweight global state
2. **React Query / TanStack Query** - Server state caching
3. **Jotai** - Atomic state management

For now, React hooks + localStorage are sufficient.

---

*State management patterns ensure predictable, maintainable state handling across the application.*
