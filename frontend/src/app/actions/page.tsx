'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, GlassCard } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button, AnimatedButton } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { ActionCard } from '@/components/action-card';
import { ZoneSelector } from '@/components/zone-selector';
import { ProfileSelector } from '@/components/profile-selector';
import { RiskBadge } from '@/components/risk-badge';
import { TrendIndicator } from '@/components/trend-indicator';
import { AnimatedCounter } from '@/components/ui/animated-counter';
import { useGSAP, gsap, prefersReducedMotion } from '@/lib/animations';
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
  Loader2,
  Sparkles
} from 'lucide-react';

// Demo recommended actions for fallback
const DEMO_ACTIONS: RecommendedActionsResponse = {
  zone_id: 'texas',
  profile: 'government',
  context: {
    spi: -1.55,
    risk_level: 'HIGH',
    trend: 'WORSENING',
    days_to_critical: 32,
    profile: 'government',
    zone: 'texas',
  },
  activated_heuristics: [
    { id: 'H4', priority: 1, actions_count: 2 },
    { id: 'H2', priority: 2, actions_count: 1 },
  ],
  actions: [
    {
      action_instance_id: 'demo-instance-1',
      action_code: 'H4_LAWN_BAN',
      title: 'Lawn/Garden Irrigation Restriction',
      description: 'Prohibit or restrict lawn and garden irrigation during peak drought periods.',
      heuristic_id: 'H4',
      priority_score: 85,
      parameters: { reduction_percentage: 15, duration_days: 30 },
      justification: 'SPI -1.72, WORSENING trend, 24 days to critical. Non-essential use reduction critical.',
      expected_effect: { days_gained: 19, confidence: 'estimated', formula: '1% removed → +1.3 days' },
      method: 'demo',
    },
    {
      action_instance_id: 'demo-instance-2',
      action_code: 'H2_PRESSURE_REDUCTION',
      title: 'Network Pressure Management',
      description: 'Reduce water pressure in distribution network to minimize losses and consumption.',
      heuristic_id: 'H2',
      priority_score: 72,
      parameters: { pressure_reduction_percent: 10, target_zones: ['residential'] },
      justification: 'Pressure management reduces both consumption and leak losses.',
      expected_effect: { days_gained: 4, confidence: 'estimated', formula: '10% pressure → +4 days' },
      method: 'demo',
    },
    {
      action_instance_id: 'demo-instance-3',
      action_code: 'H4_CARWASH_RESTRICTION',
      title: 'Car Wash Restrictions',
      description: 'Limit commercial and residential car washing to reduce non-essential water use.',
      heuristic_id: 'H4',
      priority_score: 65,
      parameters: { allowed_days: ['saturday', 'sunday'], commercial_closed: true },
      justification: 'Car washing is discretionary use that can be safely restricted.',
      expected_effect: { days_gained: 1, confidence: 'estimated', formula: '0.5% → +0.65 days' },
      method: 'demo',
    },
  ],
};

// Type for storing selected action info
interface SelectedAction {
  action_instance_id: string;
  action_code: string;
  title: string;
  days_gained: number;
}

export default function ActionsPage() {
  const router = useRouter();
  const [zones, setZones] = useState<Zone[]>(DEMO_ZONES);
  const [selectedZone, setSelectedZone] = useState<string>('texas');
  const [selectedProfile, setSelectedProfile] = useState<Profile>('government');
  const [recommendations, setRecommendations] = useState<RecommendedActionsResponse | null>(null);
  const [selectedActions, setSelectedActions] = useState<Map<string, SelectedAction>>(new Map());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  const cardsRef = useRef<HTMLDivElement>(null);

  // Fetch zones from API on mount
  useEffect(() => {
    async function fetchZones() {
      try {
        const response = await api.getZones();
        if (response.zones && response.zones.length > 0) {
          setZones(response.zones);
        }
      } catch (err) {
        console.warn('Failed to fetch zones, using demo data:', err);
      }
    }
    fetchZones();
  }, []);

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

  // GSAP animation for cards
  useGSAP(() => {
    if (prefersReducedMotion() || loading || !recommendations) return;

    if (cardsRef.current) {
      gsap.fromTo(cardsRef.current.querySelectorAll('.action-card-wrapper'),
        { opacity: 0, y: 30, scale: 0.98 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.5,
          stagger: 0.1,
          ease: 'power2.out',
        }
      );
    }
  }, { dependencies: [loading, recommendations] });

  const toggleAction = (actionInstanceId: string) => {
    const action = recommendations?.actions.find(a => a.action_instance_id === actionInstanceId);
    if (!action) return;
    
    setSelectedActions(prev => {
      const next = new Map(prev);
      if (next.has(actionInstanceId)) {
        next.delete(actionInstanceId);
      } else {
        next.set(actionInstanceId, {
          action_instance_id: action.action_instance_id,
          action_code: action.action_code,
          title: action.title,
          days_gained: action.expected_effect.days_gained,
        });
      }
      return next;
    });
  };

  const proceedToSimulation = () => {
    const actionsArray = Array.from(selectedActions.values());
    localStorage.setItem('selectedActions', JSON.stringify(actionsArray));
    localStorage.setItem('selectedZone', selectedZone);
    router.push('/simulation');
  };

  const totalDaysGained = Array.from(selectedActions.values())
    .reduce((sum, a) => sum + a.days_gained, 0);

  return (
    <div className="container py-8">
      {/* Header */}
      <motion.div 
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div>
          <span className="text-sm font-semibold text-primary mb-1 block tracking-wide uppercase">
            Action Recommendations
          </span>
          <h1 className="text-3xl font-bold tracking-tight">Smart Actions</h1>
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
      </motion.div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Alert className="mb-6 bg-primary/5 border-primary/20">
            <Info className="h-4 w-4 text-primary" />
            <AlertTitle className="text-primary">Demo Mode</AlertTitle>
            <AlertDescription>
              Showing sample recommendations. Connect to API for AI-parameterized actions.
            </AlertDescription>
          </Alert>
        </motion.div>
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
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <Card className="mb-8">
            <CardHeader className="pb-3">
              <CardTitle className="text-base flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                Current Context
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap items-center gap-4 md:gap-6">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Risk:</span>
                  <RiskBadge level={recommendations.context.risk_level} />
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">SPI:</span>
                  <span className="font-mono font-semibold text-foreground">{recommendations.context.spi.toFixed(2)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Trend:</span>
                  <TrendIndicator trend={recommendations.context.trend} size="sm" />
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Days to Critical:</span>
                  <span className="font-mono font-semibold text-red-600">
                    ~{recommendations.context.days_to_critical}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Heuristics:</span>
                  <div className="flex gap-1">
                    {recommendations.activated_heuristics.map(h => (
                      <Badge key={h.id} variant="outline" className="text-xs">{h.id}</Badge>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Loading State */}
      {loading ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="animate-pulse">
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
          <div ref={cardsRef} className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 mb-8">
            {recommendations.actions.map((action) => (
              <div key={action.action_instance_id} className="action-card-wrapper">
                <ActionCard
                  action={action}
                  selected={selectedActions.has(action.action_instance_id)}
                  onToggle={() => toggleAction(action.action_instance_id)}
                />
              </div>
            ))}
          </div>

          {/* Empty State */}
          {selectedActions.size === 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <Card className="border-dashed border-2">
                <CardContent className="py-12 text-center">
                  <div className="w-16 h-16 rounded-2xl bg-secondary flex items-center justify-center mx-auto mb-4">
                    <Zap className="h-8 w-8 text-muted-foreground" />
                  </div>
                  <p className="font-semibold text-lg mb-1">Select actions to simulate</p>
                  <p className="text-sm text-muted-foreground">
                    Click on action cards above to select them for simulation
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </>
      ) : null}

      {/* Floating Selection Summary & CTA */}
      <AnimatePresence>
        {selectedActions.size > 0 && (
          <motion.div
            className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 w-full max-w-2xl px-4"
            initial={{ opacity: 0, y: 50, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.95 }}
            transition={{ 
              type: 'spring', 
              stiffness: 400, 
              damping: 30 
            }}
          >
            <div className="glass rounded-2xl shadow-2xl border border-border/60 p-4">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <div className="p-2 rounded-xl bg-primary/10">
                      <CheckCircle2 className="h-5 w-5 text-primary" />
                    </div>
                    <span className="font-semibold">
                      {selectedActions.size} action{selectedActions.size > 1 ? 's' : ''} selected
                    </span>
                  </div>
                  <div className="h-8 w-px bg-border hidden sm:block" />
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Est. days gained:</span>
                    <span className="text-2xl font-bold text-emerald-600">
                      +<AnimatedCounter value={totalDaysGained} />
                    </span>
                  </div>
                </div>
                <AnimatedButton 
                  onClick={proceedToSimulation} 
                  size="lg"
                  className="gap-2 shadow-lg shadow-primary/25"
                >
                  <Zap className="h-4 w-4" />
                  Simulate Scenario
                  <ArrowRight className="h-4 w-4" />
                </AnimatedButton>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
