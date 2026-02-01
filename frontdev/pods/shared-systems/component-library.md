# Component Library

**Shared Systems Pod — Frontend Decision Intelligence Engineering Organization**

---

## Overview

This document catalogs the reusable components available in the frontend.

---

## Component Architecture

```
frontend/src/components/
├── ui/                    # shadcn/ui base components
│   ├── button.tsx
│   ├── card.tsx
│   ├── badge.tsx
│   ├── select.tsx
│   ├── alert.tsx
│   ├── skeleton.tsx
│   ├── progress.tsx
│   ├── tabs.tsx
│   └── separator.tsx
│
├── risk-badge.tsx         # Risk level badge
├── risk-card.tsx          # Risk assessment card
├── trend-indicator.tsx    # Trend direction indicator
├── action-card.tsx        # Recommended action card
├── navigation.tsx         # Main navigation header
├── zone-selector.tsx      # Zone dropdown
└── profile-selector.tsx   # Profile dropdown
```

---

## Base Components (shadcn/ui)

These are from shadcn/ui and should be used as building blocks.

### Button

```tsx
import { Button } from '@/components/ui/button';

<Button variant="default">Primary Action</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>
```

### Card

```tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description text</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
</Card>
```

### Badge

```tsx
import { Badge } from '@/components/ui/badge';

<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Destructive</Badge>
```

### Select

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

<Select value={value} onValueChange={setValue}>
  <SelectTrigger>
    <SelectValue placeholder="Select..." />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="option1">Option 1</SelectItem>
    <SelectItem value="option2">Option 2</SelectItem>
  </SelectContent>
</Select>
```

### Alert

```tsx
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { AlertCircle, Info } from 'lucide-react';

<Alert>
  <Info className="h-4 w-4" />
  <AlertTitle>Info</AlertTitle>
  <AlertDescription>Informational message</AlertDescription>
</Alert>

<Alert variant="destructive">
  <AlertCircle className="h-4 w-4" />
  <AlertTitle>Error</AlertTitle>
  <AlertDescription>Error message</AlertDescription>
</Alert>
```

### Skeleton

```tsx
import { Skeleton } from '@/components/ui/skeleton';

<Skeleton className="h-4 w-24" />
<Skeleton className="h-8 w-full" />
```

---

## Custom Components

### RiskBadge

Displays risk level with appropriate color coding.

```tsx
import { RiskBadge } from '@/components/risk-badge';

<RiskBadge level="CRITICAL" />           // Red
<RiskBadge level="HIGH" />               // Orange
<RiskBadge level="MEDIUM" />             // Amber
<RiskBadge level="LOW" />                // Green

// Props
interface RiskBadgeProps {
  level: RiskLevel;          // 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  size?: 'sm' | 'md' | 'lg'; // Default: 'md'
  pulse?: boolean;           // Animate critical level
}
```

### TrendIndicator

Shows trend direction with icon and label.

```tsx
import { TrendIndicator } from '@/components/trend-indicator';

<TrendIndicator trend="IMPROVING" />  // Green up arrow
<TrendIndicator trend="STABLE" />     // Gray minus
<TrendIndicator trend="WORSENING" />  // Red down arrow

// Props
interface TrendIndicatorProps {
  trend: Trend;              // 'IMPROVING' | 'STABLE' | 'WORSENING'
  showLabel?: boolean;       // Default: true
  size?: 'sm' | 'md' | 'lg'; // Default: 'md'
}
```

### RiskCard

Complete risk assessment display card.

```tsx
import { RiskCard } from '@/components/risk-card';

<RiskCard risk={riskData} zoneName="Mexico City" />

// Props
interface RiskCardProps {
  risk: RiskResponse;
  zoneName: string;
}

// Features:
// - Shows SPI-6 value
// - Days to critical with urgency indicator
// - Trend indicator
// - Urgency bar for < 30 days
```

### ActionCard

Displays recommended action with selection support.

```tsx
import { ActionCard } from '@/components/action-card';

<ActionCard
  action={recommendedAction}
  selected={isSelected}
  onToggle={handleToggle}
/>

// Props
interface ActionCardProps {
  action: RecommendedAction;
  selected?: boolean;
  onToggle?: (code: string) => void;
}

// Features:
// - Priority score badge
// - Heuristic ID
// - Expected effect (days gained)
// - AI method indicator
// - Justification text
// - Selection state
```

### ZoneSelector

Dropdown for zone selection.

```tsx
import { ZoneSelector } from '@/components/zone-selector';

<ZoneSelector
  zones={zones}
  value={selectedZone}
  onChange={setSelectedZone}
/>

// Props
interface ZoneSelectorProps {
  zones: Zone[];
  value: string;
  onChange: (value: string) => void;
}
```

### ProfileSelector

Dropdown for user profile selection.

```tsx
import { ProfileSelector } from '@/components/profile-selector';

<ProfileSelector
  value={selectedProfile}
  onChange={setSelectedProfile}
/>

// Props
interface ProfileSelectorProps {
  value: Profile;  // 'government' | 'industry'
  onChange: (value: Profile) => void;
}
```

### Navigation

Main application navigation header.

```tsx
import { Navigation } from '@/components/navigation';

// In layout.tsx
<Navigation />

// Features:
// - Logo with link to home
// - Nav links: Home, Risk, Actions, Simulation
// - Active state highlighting
// - Responsive (icons on mobile, full labels on desktop)
```

---

## Component Patterns

### Conditional Classes with cn()

```tsx
import { cn } from '@/lib/utils';

<Card className={cn(
  'transition-all duration-200',
  isSelected && 'ring-2 ring-primary',
  isUrgent && 'border-red-200'
)}>
```

### Loading States

```tsx
if (loading) {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-5 w-3/4" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-24" />
        <Skeleton className="h-4 w-full mt-2" />
      </CardContent>
    </Card>
  );
}
```

### Error States

```tsx
if (error) {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>Error</AlertTitle>
      <AlertDescription>{error}</AlertDescription>
    </Alert>
  );
}
```

### Empty States

```tsx
if (!data || data.length === 0) {
  return (
    <Card className="border-dashed">
      <CardContent className="py-8 text-center">
        <Icon className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
        <p className="font-medium">No data available</p>
        <p className="text-sm text-muted-foreground mt-1">
          Description of what to do
        </p>
      </CardContent>
    </Card>
  );
}
```

---

## Icons (Lucide)

We use Lucide React for icons:

```tsx
import { 
  Droplets,      // Water/SPI
  BarChart3,     // Risk/Charts
  Zap,           // Actions
  Play,          // Simulation
  Clock,         // Time/Days
  TrendingUp,    // Improving
  TrendingDown,  // Worsening
  AlertTriangle, // Warning
  CheckCircle2,  // Success/Selected
  XCircle,       // Error/Unselected
  Info,          // Information
  AlertCircle,   // Alert
  Loader2,       // Loading spinner
  ArrowRight,    // Navigation
  ChevronLeft,   // Back
} from 'lucide-react';

<Droplets className="h-5 w-5" />
<Loader2 className="h-4 w-4 animate-spin" />
```

---

## Adding New Components

1. Create file in `frontend/src/components/`
2. Follow naming convention (`kebab-case.tsx`)
3. Define props interface
4. Add JSDoc comment
5. Export from component file
6. Document in this file

---

*Component library provides consistent, reusable building blocks for the decision interface.*
