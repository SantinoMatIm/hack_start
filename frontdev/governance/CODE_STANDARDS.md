# Code Standards

**Frontend Decision Intelligence Engineering Organization**

---

## Purpose

This document defines the code quality standards for all frontend work. These standards ensure consistency, maintainability, and alignment with the platform's decision-support mission.

---

## Language & Framework Standards

### TypeScript

| Standard | Requirement |
|----------|-------------|
| TypeScript version | 5.0+ |
| Strict mode | Enabled (`"strict": true`) |
| No `any` | Avoid; use `unknown` or proper types |
| Explicit return types | Required for exported functions |
| Imports | Use path aliases (`@/`) |

### React/Next.js

| Standard | Requirement |
|----------|-------------|
| Next.js version | 16+ with App Router |
| Components | Functional components only |
| Server vs Client | Use `'use client'` directive only when needed |
| Hooks | Follow Rules of Hooks |

### Code Style

```typescript
// Good: Clear, typed, documented
interface RiskCardProps {
  risk: RiskResponse;
  zoneName: string;
}

/**
 * Displays the primary risk assessment card.
 * Shows SPI, risk level, trend, and days to critical.
 */
export function RiskCard({ risk, zoneName }: RiskCardProps) {
  const isUrgent = risk.days_to_critical < 30;
  
  return (
    <Card className={cn(
      'relative overflow-hidden',
      isUrgent && 'border-red-200'
    )}>
      {/* ... */}
    </Card>
  );
}

// Bad: Unclear, untyped, undocumented
export function Card({ data, flag = true }: any) {
  // ...
}
```

---

## File Organization

### Page Structure

```typescript
// frontend/src/app/{route}/page.tsx

'use client'; // Only if client-side interactivity needed

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { api, type RiskResponse } from '@/lib/api';

export default function RiskPage() {
  const [risk, setRisk] = useState<RiskResponse | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    async function fetchData() {
      try {
        const data = await api.getCurrentRisk('cdmx');
        setRisk(data);
      } catch (error) {
        console.error('Failed to fetch risk:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);
  
  if (loading) return <LoadingSkeleton />;
  if (!risk) return <ErrorState />;
  
  return (
    <div className="container py-8">
      {/* Page content */}
    </div>
  );
}
```

### Component Structure

```typescript
// frontend/src/components/risk-badge.tsx

'use client';

import { Badge } from '@/components/ui/badge';
import type { RiskLevel } from '@/lib/api/types';
import { cn } from '@/lib/utils';

interface RiskBadgeProps {
  level: RiskLevel;
  size?: 'sm' | 'md' | 'lg';
  pulse?: boolean;
}

const riskConfig: Record<RiskLevel, { label: string; className: string }> = {
  CRITICAL: {
    label: 'Critical',
    className: 'bg-red-100 text-red-700 border-red-200',
  },
  // ... other levels
};

/**
 * Displays a risk level badge with appropriate styling.
 */
export function RiskBadge({ level, size = 'md', pulse = false }: RiskBadgeProps) {
  const config = riskConfig[level];
  
  return (
    <Badge
      variant="outline"
      className={cn(
        config.className,
        pulse && level === 'CRITICAL' && 'animate-pulse'
      )}
    >
      {config.label}
    </Badge>
  );
}
```

---

## Naming Conventions

### Files

| Type | Convention | Example |
|------|------------|---------|
| Pages | `{route}/page.tsx` | `risk/page.tsx` |
| Components | `{kebab-case}.tsx` | `risk-badge.tsx` |
| UI Components | `{kebab-case}.tsx` in `ui/` | `ui/button.tsx` |
| Utilities | `{kebab-case}.ts` | `api-client.ts` |
| Types | `types.ts` | `lib/api/types.ts` |

### Components & Functions

| Type | Convention | Example |
|------|------------|---------|
| React Components | PascalCase | `RiskCard`, `ActionCard` |
| Hooks | camelCase with `use` prefix | `useRiskData`, `useActions` |
| Utilities | camelCase | `formatDate`, `calculateDays` |
| Event handlers | camelCase with `handle` prefix | `handleSelect`, `handleSubmit` |
| API functions | camelCase with verb prefix | `getCurrentRisk`, `simulateScenario` |

### Variables & Types

| Type | Convention | Example |
|------|------------|---------|
| Interfaces | PascalCase | `RiskResponse`, `ActionCard` |
| Type aliases | PascalCase | `RiskLevel`, `Trend` |
| Constants | UPPER_SNAKE_CASE | `MAX_PROJECTION_DAYS` |
| Variables | camelCase | `selectedZone`, `isLoading` |

### CSS Classes (Tailwind)

Use Tailwind utilities directly. For custom classes:

| Type | Convention | Example |
|------|------------|---------|
| Components | kebab-case | `risk-card` |
| Modifiers | Tailwind variants | `hover:bg-primary` |
| States | data attributes | `data-[state=active]:bg-primary` |

---

## State Management

### React State

```typescript
// Local component state
const [selectedZone, setSelectedZone] = useState<string>('cdmx');
const [risk, setRisk] = useState<RiskResponse | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);
```

### Persistence (localStorage)

```typescript
// Save to localStorage for cross-page state
const saveSelectedActions = (actions: string[]) => {
  localStorage.setItem('selectedActions', JSON.stringify(actions));
};

const loadSelectedActions = (): string[] => {
  const stored = localStorage.getItem('selectedActions');
  return stored ? JSON.parse(stored) : [];
};
```

### URL State (for shareable state)

```typescript
// Use Next.js searchParams for shareable state
import { useSearchParams } from 'next/navigation';

export default function RiskPage() {
  const searchParams = useSearchParams();
  const zone = searchParams.get('zone') || 'cdmx';
  // ...
}
```

---

## API Integration

### Client Usage

```typescript
import { api, type RiskResponse } from '@/lib/api';

// In a component
const [risk, setRisk] = useState<RiskResponse | null>(null);

useEffect(() => {
  async function fetchRisk() {
    try {
      const data = await api.getCurrentRisk(selectedZone);
      setRisk(data);
    } catch (error) {
      // Fallback to demo data
      setRisk(api.getDemoRisk(selectedZone));
      setIsDemo(true);
    }
  }
  fetchRisk();
}, [selectedZone]);
```

### Error Handling

```typescript
// Good: Graceful degradation with user feedback
try {
  const result = await api.getRecommendedActions({ zone_id, profile });
  setActions(result.actions);
} catch (error) {
  console.error('API error:', error);
  // Show demo data with clear indication
  setActions(DEMO_ACTIONS);
  setIsDemo(true);
}

// In JSX:
{isDemo && (
  <Alert>
    <Info className="h-4 w-4" />
    <AlertTitle>Demo Mode</AlertTitle>
    <AlertDescription>
      Showing sample data. Connect to API for live results.
    </AlertDescription>
  </Alert>
)}
```

---

## Component Patterns

### shadcn/ui Usage

```typescript
// Always import from @/components/ui/
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

// Use cn() for conditional classes
import { cn } from '@/lib/utils';

<Card className={cn(
  'transition-all duration-200',
  isSelected && 'ring-2 ring-primary'
)}>
```

### Props Interface Pattern

```typescript
interface ActionCardProps {
  action: RecommendedAction;
  selected?: boolean;
  onToggle?: (code: string) => void;
}

export function ActionCard({ 
  action, 
  selected = false, 
  onToggle 
}: ActionCardProps) {
  // ...
}
```

### Conditional Rendering

```typescript
// Good: Clear conditional logic
{loading && <Skeleton className="h-8 w-24" />}
{error && <ErrorAlert message={error} />}
{risk && <RiskDisplay risk={risk} />}

// Good: Early returns for states
if (loading) return <LoadingSkeleton />;
if (error) return <ErrorState error={error} />;
if (!data) return <EmptyState />;

return <MainContent data={data} />;
```

---

## Comments & Documentation

### When to Comment

```typescript
// Comment on WHY, not WHAT
// Bad: Increment counter
counter += 1;

// Good: Track API calls for rate limiting (max 10/minute)
counter += 1;
```

### JSDoc for Exported Functions

```typescript
/**
 * Fetches the current risk assessment for a zone.
 * Falls back to demo data if API is unavailable.
 * 
 * @param zoneId - Zone identifier (e.g., 'cdmx', 'monterrey')
 * @returns Risk response with SPI, level, trend, and days to critical
 */
export async function getCurrentRisk(zoneId: string): Promise<RiskResponse> {
  // ...
}
```

### TODO Comments

```typescript
// TODO(session-id): Brief description of needed work
// Example:
// TODO(2026-01-31-urgency): Add animation for days-to-critical countdown
```

---

## Testing Considerations

### Component Testability

```typescript
// Good: Logic separated from rendering
function calculateUrgencyLevel(daysToCritical: number): string {
  if (daysToCritical < 15) return 'critical';
  if (daysToCritical < 30) return 'high';
  if (daysToCritical < 45) return 'medium';
  return 'low';
}

// This pure function can be easily unit tested
```

### Data Validation

```typescript
function validateRiskData(data: unknown): data is RiskResponse {
  if (!data || typeof data !== 'object') return false;
  const d = data as Record<string, unknown>;
  return (
    typeof d.zone_id === 'string' &&
    typeof d.spi_6m === 'number' &&
    ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].includes(d.risk_level as string)
  );
}
```

---

## Performance Guidelines

### Avoid Unnecessary Re-renders

```typescript
// Use useMemo for expensive computations
const sortedActions = useMemo(() => 
  actions.sort((a, b) => b.priority_score - a.priority_score),
  [actions]
);

// Use useCallback for callback props
const handleToggle = useCallback((code: string) => {
  setSelected(prev => 
    prev.has(code) 
      ? new Set([...prev].filter(c => c !== code))
      : new Set([...prev, code])
  );
}, []);
```

### Lazy Loading

```typescript
// Dynamic imports for heavy components
import dynamic from 'next/dynamic';

const SimulationChart = dynamic(
  () => import('@/components/simulation-chart'),
  { loading: () => <Skeleton className="h-[400px]" /> }
);
```

### Image Optimization

```typescript
// Use Next.js Image component
import Image from 'next/image';

<Image 
  src="/logo.png" 
  alt="Water Risk Platform" 
  width={120} 
  height={40}
  priority // For above-fold images
/>
```

---

## Code Review Checklist

Before Phase 3 Fidelity Review, verify:

- [ ] TypeScript strict mode passes
- [ ] No `any` types without justification
- [ ] All exported functions have JSDoc
- [ ] Props interfaces defined for all components
- [ ] Error handling for all API calls
- [ ] Loading and empty states handled
- [ ] Tailwind classes used (no inline styles)
- [ ] Accessibility: alt text, ARIA labels, focus states
- [ ] No hardcoded values (use constants or config)
- [ ] Comments explain WHY, not WHAT
- [ ] Performance: useMemo/useCallback where appropriate

---

*Code standards ensure maintainable, consistent frontend code that serves the decision-support mission.*
