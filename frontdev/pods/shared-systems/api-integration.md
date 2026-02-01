# API Integration Patterns

**Shared Systems Pod — Frontend Decision Intelligence Engineering Organization**

---

## Overview

This document defines patterns for integrating with the FastAPI backend from the Next.js frontend.

---

## API Client Architecture

```
frontend/src/lib/api/
├── client.ts      # API functions (fetch wrappers)
├── types.ts       # TypeScript interfaces matching backend schemas
└── index.ts       # Re-exports for clean imports
```

### Client Structure

```typescript
// frontend/src/lib/api/client.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
}

// Exported functions
export async function getCurrentRisk(zoneId: string): Promise<RiskResponse> {
  return fetchApi(`/risk/current?zone_id=${zoneId}`);
}
```

---

## Usage Patterns

### Basic Data Fetching

```typescript
'use client';

import { useEffect, useState } from 'react';
import { api, type RiskResponse } from '@/lib/api';

export function RiskDisplay({ zoneId }: { zoneId: string }) {
  const [risk, setRisk] = useState<RiskResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRisk() {
      try {
        setLoading(true);
        const data = await api.getCurrentRisk(zoneId);
        setRisk(data);
        setError(null);
      } catch (err) {
        setError('Failed to fetch risk data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    
    fetchRisk();
  }, [zoneId]);

  if (loading) return <Skeleton />;
  if (error) return <ErrorAlert message={error} />;
  if (!risk) return null;
  
  return <RiskCard risk={risk} />;
}
```

### With Demo Mode Fallback

```typescript
useEffect(() => {
  async function fetchData() {
    setLoading(true);
    
    try {
      const data = await api.getRecommendedActions({
        zone_id: selectedZone,
        profile: selectedProfile,
      });
      setActions(data.actions);
      setIsDemo(false);
    } catch (err) {
      // Fallback to demo data
      console.warn('API unavailable, using demo data');
      setActions(DEMO_ACTIONS);
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  }
  
  fetchData();
}, [selectedZone, selectedProfile]);
```

### POST Requests

```typescript
async function runSimulation() {
  setLoading(true);
  
  try {
    const result = await api.simulateScenario({
      zone_id: selectedZone,
      action_codes: Array.from(selectedActions),
      projection_days: 90,
    });
    setSimulation(result);
  } catch (err) {
    setError('Simulation failed');
  } finally {
    setLoading(false);
  }
}
```

---

## Type Safety

### Matching Backend Schemas

Types in `types.ts` must match FastAPI Pydantic models:

```typescript
// Must match src/api/schemas/risk.py
export interface RiskResponse {
  zone_id: string;
  spi_6m: number;
  risk_level: RiskLevel;
  trend: Trend;
  days_to_critical: number;
  last_updated: string;
}

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type Trend = 'IMPROVING' | 'STABLE' | 'WORSENING';
```

### Import Pattern

```typescript
// Clean imports from single entry point
import { 
  api,
  type RiskResponse,
  type RecommendedAction,
  type SimulationResponse,
} from '@/lib/api';
```

---

## Error Handling

### Standard Pattern

```typescript
try {
  const data = await api.getCurrentRisk(zoneId);
  // Handle success
} catch (error) {
  if (error instanceof Error) {
    // Known error type
    setError(error.message);
  } else {
    // Unknown error
    setError('An unexpected error occurred');
  }
}
```

### User Feedback

Always provide clear feedback:

```tsx
{error && (
  <Alert variant="destructive">
    <AlertCircle className="h-4 w-4" />
    <AlertTitle>Error</AlertTitle>
    <AlertDescription>{error}</AlertDescription>
  </Alert>
)}
```

---

## Demo Mode

### When to Use

- API server unavailable
- Offline development
- Demonstrations without live data

### Implementation

```typescript
// In client.ts
export const DEMO_RISK_CDMX: RiskResponse = {
  zone_id: 'cdmx',
  spi_6m: -1.72,
  risk_level: 'HIGH',
  trend: 'WORSENING',
  days_to_critical: 24,
  last_updated: new Date().toISOString(),
};

export function getDemoRisk(zoneId: string): RiskResponse {
  return zoneId === 'cdmx' ? DEMO_RISK_CDMX : DEMO_RISK_MONTERREY;
}
```

### Visual Indication

```tsx
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

## Environment Configuration

### Required Variables

```env
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production

```env
# Production
NEXT_PUBLIC_API_URL=https://api.waterrisk.example.com
```

---

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/zones` | GET | List zones |
| `/zones/{id}` | GET | Get zone details |
| `/risk/current` | GET | Current risk assessment |
| `/risk/history` | GET | Historical risk data |
| `/actions` | GET | Action catalog |
| `/actions/recommended` | POST | AI recommendations |
| `/scenarios/simulate` | POST | Run simulation |

---

*API integration patterns ensure consistent, type-safe communication with the backend.*
