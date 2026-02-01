'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { ActionCard } from '@/components/action-card';
import { ZoneSelector } from '@/components/zone-selector';
import { ProfileSelector } from '@/components/profile-selector';
import { RiskBadge } from '@/components/risk-badge';
import { TrendIndicator } from '@/components/trend-indicator';
import { 
  api, 
  DEMO_ZONES,
  type Zone,
  type Profile,
  type RecommendedActionsResponse,
} from '@/lib/api';
import { 
  AlertCircle, 
  Info,
  Zap,
  ArrowRight,
  CheckCircle2,
  Loader2
} from 'lucide-react';

// Demo recommended actions for fallback
const DEMO_ACTIONS: RecommendedActionsResponse = {
  zone_id: 'cdmx',
  profile: 'government',
  context: {
    spi: -1.72,
    risk_level: 'HIGH',
    trend: 'WORSENING',
    days_to_critical: 24,
    profile: 'government',
    zone: 'cdmx',
  },
  activated_heuristics: [
    { id: 'H4', priority: 1, actions_count: 2 },
    { id: 'H2', priority: 2, actions_count: 1 },
  ],
  actions: [
    {
      action_code: 'H4_LAWN_BAN',
      title: 'Lawn/Garden Irrigation Restriction',
      description: 'Prohibit or restrict lawn and garden irrigation during peak drought periods.',
      heuristic_id: 'H4',
      priority_score: 85,
      parameters: { reduction_percentage: 15, duration_days: 30 },
      justification: 'SPI -1.72, WORSENING trend, 24 days to critical. Non-essential use reduction critical.',
      expected_effect: { days_gained: 19, confidence: 'estimated', formula: '1% removed → +1.3 days' },
      method: 'ai',
    },
    {
      action_code: 'H2_PRESSURE_REDUCTION',
      title: 'Network Pressure Management',
      description: 'Reduce water pressure in distribution network to minimize losses and consumption.',
      heuristic_id: 'H2',
      priority_score: 72,
      parameters: { pressure_reduction_percent: 10, target_zones: ['residential'] },
      justification: 'Pressure management reduces both consumption and leak losses.',
      expected_effect: { days_gained: 4, confidence: 'estimated', formula: '10% pressure → +4 days' },
      method: 'ai',
    },
    {
      action_code: 'H4_CARWASH_RESTRICTION',
      title: 'Car Wash Restrictions',
      description: 'Limit commercial and residential car washing to reduce non-essential water use.',
      heuristic_id: 'H4',
      priority_score: 65,
      parameters: { allowed_days: ['saturday', 'sunday'], commercial_closed: true },
      justification: 'Car washing is discretionary use that can be safely restricted.',
      expected_effect: { days_gained: 1, confidence: 'estimated', formula: '0.5% → +0.65 days' },
      method: 'fallback',
    },
  ],
};

export default function ActionsPage() {
  const router = useRouter();
  const [zones] = useState<Zone[]>(DEMO_ZONES);
  const [selectedZone, setSelectedZone] = useState<string>('cdmx');
  const [selectedProfile, setSelectedProfile] = useState<Profile>('government');
  const [recommendations, setRecommendations] = useState<RecommendedActionsResponse | null>(null);
  const [selectedActions, setSelectedActions] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.getRecommendedActions({
        zone_id: selectedZone,
        profile: selectedProfile,
      });
      setRecommendations(data);
      setIsDemo(false);
    } catch (err) {
      console.warn('API unavailable, using demo data:', err);
      setRecommendations({
        ...DEMO_ACTIONS,
        zone_id: selectedZone,
        profile: selectedProfile,
        context: { ...DEMO_ACTIONS.context, profile: selectedProfile, zone: selectedZone },
      });
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [selectedZone, selectedProfile]);

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

  const proceedToSimulation = () => {
    // Store selected actions in localStorage for simulation page
    localStorage.setItem('selectedActions', JSON.stringify(Array.from(selectedActions)));
    localStorage.setItem('selectedZone', selectedZone);
    router.push('/simulation');
  };

  const totalDaysGained = recommendations?.actions
    .filter(a => selectedActions.has(a.action_code))
    .reduce((sum, a) => sum + a.expected_effect.days_gained, 0) || 0;

  return (
    <div className="container py-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Recommended Actions</h1>
          <p className="text-muted-foreground mt-1">
            AI-parameterized actions based on current risk context
          </p>
        </div>
        <div className="flex items-center gap-3">
          <ZoneSelector 
            zones={zones} 
            value={selectedZone} 
            onChange={setSelectedZone} 
          />
          <ProfileSelector
            value={selectedProfile}
            onChange={setSelectedProfile}
          />
        </div>
      </div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <Alert className="mb-6">
          <Info className="h-4 w-4" />
          <AlertTitle>Demo Mode</AlertTitle>
          <AlertDescription>
            Showing sample recommendations. Connect to API for AI-parameterized actions.
          </AlertDescription>
        </Alert>
      )}

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive" className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Context Summary */}
      {recommendations && (
        <Card className="mb-6">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Current Context</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Risk:</span>
                <RiskBadge level={recommendations.context.risk_level} />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">SPI:</span>
                <span className="font-mono font-medium">{recommendations.context.spi.toFixed(2)}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Trend:</span>
                <TrendIndicator trend={recommendations.context.trend} size="sm" />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Days to Critical:</span>
                <span className="font-mono font-medium text-red-600 dark:text-red-400">
                  ~{recommendations.context.days_to_critical}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">Heuristics:</span>
                {recommendations.activated_heuristics.map(h => (
                  <Badge key={h.id} variant="outline">{h.id}</Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Loading State */}
      {loading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(3)].map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <Skeleton className="h-5 w-3/4" />
                <Skeleton className="h-4 w-1/2" />
              </CardHeader>
              <CardContent className="space-y-3">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-12 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : recommendations ? (
        <>
          {/* Actions Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
            {recommendations.actions.map((action) => (
              <ActionCard
                key={action.action_code}
                action={action}
                selected={selectedActions.has(action.action_code)}
                onToggle={toggleAction}
              />
            ))}
          </div>

          {/* Selection Summary & CTA */}
          {selectedActions.size > 0 && (
            <Card className="sticky bottom-4 border-primary bg-background/95 backdrop-blur shadow-lg">
              <CardContent className="py-4">
                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-primary" />
                      <span className="font-medium">
                        {selectedActions.size} action{selectedActions.size > 1 ? 's' : ''} selected
                      </span>
                    </div>
                    <div className="h-6 w-px bg-border" />
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">Est. days gained:</span>
                      <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400">
                        +{totalDaysGained}
                      </span>
                    </div>
                  </div>
                  <Button onClick={proceedToSimulation} className="gap-2">
                    <Zap className="h-4 w-4" />
                    Simulate Scenario
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Empty State */}
          {selectedActions.size === 0 && (
            <Card className="border-dashed">
              <CardContent className="py-8 text-center">
                <Zap className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                <p className="font-medium">Select actions to simulate</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Click on action cards above to select them for simulation
                </p>
              </CardContent>
            </Card>
          )}
        </>
      ) : null}
    </div>
  );
}
