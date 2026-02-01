'use client';

import { useEffect, useState, useRef } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, HighlightedCard } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button, AnimatedButton } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { RiskBadge } from '@/components/risk-badge';
import { AnimatedCounter } from '@/components/ui/animated-counter';
import { useGSAP, gsap, prefersReducedMotion } from '@/lib/animations';
import { 
  api, 
  DEMO_ZONES,
  type SimulationResponse,
  type EconomicSimulationResponse,
  type PowerPlantListResponse,
} from '@/lib/api';
import { 
  AlertCircle, 
  Info,
  Play,
  ArrowRight,
  Clock,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Loader2,
  ChevronLeft,
  Sparkles,
  Target,
  DollarSign,
  Zap,
  Factory,
  Droplets,
  Building2,
  Brain,
  Lightbulb,
  AlertOctagon,
  ArrowUpRight,
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Legend,
} from 'recharts';

// Type for stored action info
interface StoredAction {
  action_instance_id: string;
  action_code: string;
  title: string;
  days_gained: number;
}

// Demo simulation response
const DEMO_SIMULATION: SimulationResponse = {
  zone_id: 'cdmx',
  no_action: {
    ending_spi: -2.15,
    ending_risk_level: 'CRITICAL',
    days_to_critical: 24,
    trajectory: Array.from({ length: 90 }, (_, i) => ({
      day: i + 1,
      projected_spi: -1.72 - (i * 0.005),
      risk_level: i < 40 ? 'HIGH' : 'CRITICAL',
      improvement_applied: false,
    })),
  },
  with_action: {
    ending_spi: -1.55,
    ending_risk_level: 'HIGH',
    days_to_critical: 52,
    trajectory: Array.from({ length: 90 }, (_, i) => ({
      day: i + 1,
      projected_spi: -1.72 + (i < 30 ? 0.003 * i : 0.003 * 30 - 0.002 * (i - 30)),
      risk_level: 'HIGH',
      improvement_applied: i < 30,
    })),
  },
  comparison: {
    days_gained: 28,
    spi_improvement: 0.6,
    risk_level_change: 'Prevented escalation to CRITICAL',
    actions_count: 2,
  },
  summary: 'Taking the selected actions is projected to gain 28 additional days before reaching critical threshold, improving SPI by 0.6 points and preventing escalation to CRITICAL risk level.',
  actions_applied: [
    { code: 'H4_LAWN_BAN', title: 'Lawn/Garden Irrigation Restriction', days_gained: 19 },
    { code: 'H2_PRESSURE_REDUCTION', title: 'Network Pressure Management', days_gained: 4 },
  ],
};

// Format USD with commas
function formatUSD(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

// Format number with commas
function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num);
}

export default function SimulationPage() {
  const [selectedActions, setSelectedActions] = useState<StoredAction[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('texas');
  const [zones, setZones] = useState(DEMO_ZONES);
  const [projectionDays, setProjectionDays] = useState<number>(90);
  const [simulation, setSimulation] = useState<SimulationResponse | null>(null);
  const [economicSimulation, setEconomicSimulation] = useState<EconomicSimulationResponse | null>(null);
  const [powerPlants, setPowerPlants] = useState<PowerPlantListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);
  const [simulationMode, setSimulationMode] = useState<'economic' | 'spi'>('economic');

  const resultsRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<HTMLDivElement>(null);

  // Fetch zones on mount (sequential to avoid overwhelming Supabase)
  useEffect(() => {
    async function fetchInitialData() {
      try {
        const zonesResponse = await api.getZones();
        if (zonesResponse.zones && zonesResponse.zones.length > 0) {
          setZones(zonesResponse.zones);
        }
      } catch (err) {
        console.warn('Failed to fetch zones, using demo data:', err);
      }
    }
    fetchInitialData();
  }, []);

  // Fetch power plants when zone changes (separate effect to avoid race conditions)
  useEffect(() => {
    async function fetchPowerPlants() {
      try {
        const plantsResponse = await api.getPowerPlants(selectedZone);
        setPowerPlants(plantsResponse);
      } catch (err) {
        console.warn('Failed to fetch power plants:', err);
        setPowerPlants(api.getDemoPowerPlants(selectedZone));
      }
    }
    // Small delay to avoid hitting Supabase connection limit
    const timer = setTimeout(fetchPowerPlants, 100);
    return () => clearTimeout(timer);
  }, [selectedZone]);

  useEffect(() => {
    const storedActions = localStorage.getItem('selectedActions');
    const storedZone = localStorage.getItem('selectedZone');
    
    if (storedActions) {
      const parsed = JSON.parse(storedActions);
      // Handle both old format (string[]) and new format (StoredAction[])
      if (Array.isArray(parsed) && parsed.length > 0) {
        if (typeof parsed[0] === 'string') {
          // Legacy format - convert to new format with demo IDs
          setSelectedActions(parsed.map((code: string) => ({
            action_instance_id: `legacy-${code}`,
            action_code: code,
            title: code,
            days_gained: 0,
          })));
        } else {
          setSelectedActions(parsed);
        }
      }
    }
    if (storedZone) {
      setSelectedZone(storedZone);
    }
  }, []);

  // GSAP animations for results
  useGSAP(() => {
    if (prefersReducedMotion() || loading || (!simulation && !economicSimulation)) return;

    if (resultsRef.current) {
      const tl = gsap.timeline();
      
      // Comparison cards reveal
      tl.fromTo(resultsRef.current.querySelectorAll('.comparison-card'),
        { opacity: 0, y: 30, scale: 0.98 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.6,
          stagger: 0.15,
          ease: 'power2.out',
        }
      );

      // Impact summary
      tl.fromTo('.impact-summary',
        { opacity: 0, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: 'power2.out',
        },
        '-=0.3'
      );
    }

    if (chartRef.current) {
      gsap.fromTo(chartRef.current,
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          delay: 0.5,
          ease: 'power2.out',
        }
      );
    }
  }, { dependencies: [loading, simulation, economicSimulation] });

  const runSimulation = async () => {
    setLoading(true);
    setError(null);
    
    if (simulationMode === 'economic') {
      // Economic simulation - works even without selected actions
      try {
        const data = await api.runEconomicSimulation({
          zone_id: selectedZone,
          power_plant_ids: [], // Empty = all plants in zone
          action_instance_ids: selectedActions.map(a => a.action_instance_id),
          projection_days: projectionDays,
        });
        setEconomicSimulation(data);
        setSimulation(null);
        setIsDemo(false);
      } catch (err) {
        console.warn('API unavailable, using demo data:', err);
        setEconomicSimulation(api.getDemoEconomicSimulation(selectedZone));
        setSimulation(null);
        setIsDemo(true);
      }
    } else {
      // SPI-based simulation
      if (selectedActions.length === 0) {
        setLoading(false);
        return;
      }
      
      try {
        const data = await api.simulateScenario({
          zone_id: selectedZone,
          action_instance_ids: selectedActions.map(a => a.action_instance_id),
          projection_days: projectionDays,
        });
        setSimulation(data);
        setEconomicSimulation(null);
        setIsDemo(false);
      } catch (err) {
        console.warn('API unavailable, using demo data:', err);
        setSimulation({
          ...DEMO_SIMULATION,
          comparison: {
            ...DEMO_SIMULATION.comparison,
            actions_count: selectedActions.length,
          },
          actions_applied: selectedActions.map(a => ({
            code: a.action_code,
            title: a.title,
            days_gained: a.days_gained,
          })),
        });
        setEconomicSimulation(null);
        setIsDemo(true);
      }
    }
    
    setLoading(false);
  };

  // Prepare chart data
  const chartData = simulation ? simulation.no_action.trajectory.map((point, i) => ({
    day: point.day,
    no_action: point.projected_spi,
    with_action: simulation.with_action.trajectory[i]?.projected_spi,
  })) : [];

  const zoneName = zones.find(z => z.slug === selectedZone)?.name || selectedZone;

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
          <div className="flex items-center gap-2 mb-2">
            <Link href="/actions">
              <Button variant="ghost" size="sm" className="gap-1 -ml-2">
                <ChevronLeft className="h-4 w-4" />
                Back to Actions
              </Button>
            </Link>
          </div>
          <span className="text-sm font-semibold text-primary mb-1 block tracking-wide uppercase">
            Economic Impact Analysis
          </span>
          <h1 className="text-3xl font-bold tracking-tight">Cost Simulation</h1>
          <p className="text-muted-foreground mt-1">
            Calculate potential savings from water risk mitigation on power infrastructure
          </p>
        </div>
        
        {/* Simulation Mode Toggle */}
        <div className="flex items-center gap-2">
          <Button 
            variant={simulationMode === 'economic' ? 'default' : 'outline'} 
            size="sm"
            onClick={() => setSimulationMode('economic')}
            className="gap-2"
          >
            <DollarSign className="h-4 w-4" />
            Economic
          </Button>
          <Button 
            variant={simulationMode === 'spi' ? 'default' : 'outline'} 
            size="sm"
            onClick={() => setSimulationMode('spi')}
            className="gap-2"
          >
            <Droplets className="h-4 w-4" />
            SPI-based
          </Button>
        </div>
      </motion.div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Alert className="mb-6 bg-primary/5 border-primary/20">
            <Info className="h-4 w-4 text-primary" />
            <AlertTitle className="text-primary">Demo Mode</AlertTitle>
            <AlertDescription>
              Showing simulated projections. Connect to API for actual calculations.
            </AlertDescription>
          </Alert>
        </motion.div>
      )}

      {/* Power Plants Info Card */}
      {powerPlants && powerPlants.total > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Card className="mb-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
            <CardContent className="py-4">
              <div className="flex flex-wrap items-center gap-4 md:gap-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-blue-100">
                    <Factory className="h-5 w-5 text-blue-600" />
                  </div>
                  <div>
                    <span className="text-sm text-muted-foreground">Power Plants in Zone</span>
                    <p className="font-semibold text-lg">{powerPlants.total} plants</p>
                  </div>
                </div>
                <div className="h-10 w-px bg-blue-200 hidden md:block" />
                <div>
                  <span className="text-sm text-muted-foreground">Total Capacity</span>
                  <p className="font-semibold text-lg">{formatNumber(powerPlants.total_capacity_mw)} MW</p>
                </div>
                <div className="h-10 w-px bg-blue-200 hidden md:block" />
                <div className="flex gap-2">
                  {powerPlants.plants.slice(0, 3).map(plant => (
                    <Badge key={plant.id} variant="secondary" className="text-xs">
                      {plant.name.length > 15 ? plant.name.substring(0, 15) + '...' : plant.name}
                    </Badge>
                  ))}
                  {powerPlants.total > 3 && (
                    <Badge variant="outline" className="text-xs">+{powerPlants.total - 3} more</Badge>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* No Actions Selected - Only for SPI mode */}
      {simulationMode === 'spi' && selectedActions.length === 0 ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Card className="border-dashed border-2">
            <CardContent className="py-16 text-center">
              <div className="w-20 h-20 rounded-2xl bg-amber-100 flex items-center justify-center mx-auto mb-6">
                <AlertTriangle className="h-10 w-10 text-amber-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">No Actions Selected</h3>
              <p className="text-muted-foreground mb-6 max-w-md mx-auto">
                Select actions from the Actions page to run SPI simulation, or switch to Economic mode.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button asChild size="lg">
                  <Link href="/actions">
                    Go to Actions
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </Link>
                </Button>
                <Button 
                  variant="outline" 
                  size="lg" 
                  onClick={() => setSimulationMode('economic')}
                  className="gap-2"
                >
                  <DollarSign className="h-4 w-4" />
                  Try Economic Mode
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ) : (
        <>
          {/* Simulation Parameters */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Card className="mb-8">
              <CardHeader className="pb-3">
                <CardTitle className="text-base flex items-center gap-2">
                  <Target className="h-4 w-4 text-primary" />
                  Simulation Parameters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap items-center gap-4 md:gap-6">
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Zone:</span>
                    <Badge variant="outline" className="font-medium">{zoneName}</Badge>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Mode:</span>
                    <Badge variant={simulationMode === 'economic' ? 'default' : 'secondary'} className="font-medium">
                      {simulationMode === 'economic' ? 'Economic (USD)' : 'SPI-based'}
                    </Badge>
                  </div>
                  {selectedActions.length > 0 && (
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">Actions:</span>
                      <div className="flex gap-1 flex-wrap">
                        {selectedActions.map(action => (
                          <Badge key={action.action_instance_id} variant="secondary" className="text-xs">{action.action_code}</Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Projection:</span>
                    <span className="font-semibold">{projectionDays} days</span>
                  </div>
                  <div className="ml-auto">
                    <AnimatedButton 
                      onClick={runSimulation} 
                      disabled={loading} 
                      className="gap-2"
                      size="lg"
                    >
                      {loading ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Play className="h-4 w-4" />
                      )}
                      {loading ? 'Calculating...' : 'Run Simulation'}
                    </AnimatedButton>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Loading State */}
          <AnimatePresence mode="wait">
            {loading && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="grid gap-6 md:grid-cols-2"
              >
                {[...Array(2)].map((_, i) => (
                  <Card key={i} className="animate-pulse">
                    <CardHeader>
                      <Skeleton className="h-5 w-1/2" />
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <Skeleton className="h-10 w-24" />
                      <Skeleton className="h-4 w-full" />
                      <Skeleton className="h-4 w-3/4" />
                    </CardContent>
                  </Card>
                ))}
              </motion.div>
            )}
          </AnimatePresence>

          {/* Economic Simulation Results */}
          {economicSimulation && !loading && (
            <div ref={resultsRef}>
              {/* Savings Hero Card */}
              <HighlightedCard variant="success" className="comparison-card mb-8">
                <CardContent className="py-8">
                  <div className="text-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-100 text-emerald-700 text-sm font-medium mb-4">
                      <Sparkles className="h-4 w-4" />
                      Potential Savings
                    </div>
                    <div className="text-6xl md:text-7xl font-bold text-emerald-600 mb-2">
                      {formatUSD(economicSimulation.savings_usd)}
                    </div>
                    <p className="text-lg text-muted-foreground">
                      over {economicSimulation.projection_days} days by implementing water conservation actions
                    </p>
                    <div className="flex items-center justify-center gap-2 mt-4">
                      <Badge variant="outline" className="text-emerald-600 border-emerald-300">
                        {economicSimulation.savings_pct.toFixed(1)}% cost reduction
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </HighlightedCard>

              {/* Comparison Cards */}
              <div className="grid gap-6 md:grid-cols-2 mb-8">
                {/* No Action Scenario */}
                <HighlightedCard variant="danger" className="comparison-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-red-100">
                        <XCircle className="h-5 w-5 text-red-600" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">Without Action</CardTitle>
                        <CardDescription>Projected costs if no water actions taken</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Total Cost</span>
                      <span className="text-2xl font-bold text-red-600">
                        {formatUSD(economicSimulation.no_action.total_cost_usd)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Capacity Loss</span>
                      <span className="text-xl font-semibold text-red-600">
                        {(economicSimulation.no_action.capacity_loss_pct * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Lost Generation</span>
                      <span className="font-medium">
                        {formatNumber(economicSimulation.no_action.lost_generation_mwh)} MWh
                      </span>
                    </div>
                    {economicSimulation.no_action.emergency_fuel_cost_usd > 0 && (
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-muted-foreground">Emergency Fuel</span>
                        <span className="font-medium text-amber-600">
                          {formatUSD(economicSimulation.no_action.emergency_fuel_cost_usd)}
                        </span>
                      </div>
                    )}
                  </CardContent>
                </HighlightedCard>

                {/* With Action Scenario */}
                <HighlightedCard variant="success" className="comparison-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-emerald-100">
                        <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">With Action</CardTitle>
                        <CardDescription>Projected costs with water conservation</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Total Cost</span>
                      <span className="text-2xl font-bold text-emerald-600">
                        {formatUSD(economicSimulation.with_action.total_cost_usd)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Capacity Loss</span>
                      <span className="text-xl font-semibold text-emerald-600">
                        {(economicSimulation.with_action.capacity_loss_pct * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Lost Generation</span>
                      <span className="font-medium">
                        {formatNumber(economicSimulation.with_action.lost_generation_mwh)} MWh
                      </span>
                    </div>
                    {economicSimulation.with_action.emergency_fuel_cost_usd > 0 && (
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-muted-foreground">Emergency Fuel</span>
                        <span className="font-medium text-emerald-600">
                          {formatUSD(economicSimulation.with_action.emergency_fuel_cost_usd)}
                        </span>
                      </div>
                    )}
                  </CardContent>
                </HighlightedCard>
              </div>

              {/* AI Analysis Brief */}
              {economicSimulation.ai_brief && (
                <Card className="mb-8 border-primary/20 bg-gradient-to-br from-primary/5 to-transparent">
                  <CardHeader className="pb-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-xl bg-primary/10">
                          <Brain className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">AI Analysis</CardTitle>
                          <CardDescription>
                            {economicSimulation.ai_brief.generated 
                              ? 'AI-generated insights and recommendations' 
                              : 'Analysis based on simulation data'}
                          </CardDescription>
                        </div>
                      </div>
                      {economicSimulation.ai_brief.generated && (
                        <Badge variant="outline" className="text-xs">
                          <Sparkles className="h-3 w-3 mr-1" />
                          AI Generated
                        </Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Executive Summary */}
                    <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                      <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        Executive Summary
                      </h4>
                      <p className="text-sm leading-relaxed">
                        {economicSimulation.ai_brief.executive_summary}
                      </p>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2">
                      {/* Risk Context */}
                      <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                        <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                          <AlertOctagon className="h-4 w-4" />
                          Risk Context
                        </h4>
                        <p className="text-sm leading-relaxed">
                          {economicSimulation.ai_brief.risk_context}
                        </p>
                      </div>

                      {/* Action Rationale */}
                      <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                        <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                          <Lightbulb className="h-4 w-4" />
                          Why These Actions Work
                        </h4>
                        <p className="text-sm leading-relaxed">
                          {economicSimulation.ai_brief.action_rationale}
                        </p>
                      </div>
                    </div>

                    {/* Recommendation */}
                    <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                      <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                        <ArrowUpRight className="h-4 w-4" />
                        Recommendation
                      </h4>
                      <p className="text-sm leading-relaxed">
                        {economicSimulation.ai_brief.recommendation}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Per-Plant Breakdown */}
              {economicSimulation.per_plant_breakdown.length > 0 && (
                <Card className="mb-8">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Factory className="h-5 w-5 text-primary" />
                      Per-Plant Breakdown
                    </CardTitle>
                    <CardDescription>
                      Individual impact on {economicSimulation.plants_analyzed} power plants ({formatNumber(economicSimulation.total_capacity_mw)} MW total)
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {economicSimulation.per_plant_breakdown.map((plant) => (
                        <div key={plant.plant_id} className="p-4 rounded-xl border bg-secondary/30">
                          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                            <div>
                              <h4 className="font-semibold flex items-center gap-2">
                                <Building2 className="h-4 w-4 text-muted-foreground" />
                                {plant.plant_name}
                              </h4>
                              <p className="text-sm text-muted-foreground">{formatNumber(plant.capacity_mw)} MW capacity</p>
                            </div>
                            <div className="flex flex-wrap gap-6">
                              <div className="text-center">
                                <p className="text-xs text-muted-foreground mb-1">Without Action</p>
                                <p className="font-semibold text-red-600">{formatUSD(plant.no_action_cost_usd)}</p>
                                <p className="text-xs text-muted-foreground">{(plant.capacity_loss_no_action * 100).toFixed(0)}% loss</p>
                              </div>
                              <div className="text-center">
                                <p className="text-xs text-muted-foreground mb-1">With Action</p>
                                <p className="font-semibold text-emerald-600">{formatUSD(plant.with_action_cost_usd)}</p>
                                <p className="text-xs text-muted-foreground">{(plant.capacity_loss_with_action * 100).toFixed(0)}% loss</p>
                              </div>
                              <div className="text-center">
                                <p className="text-xs text-muted-foreground mb-1">Savings</p>
                                <p className="font-bold text-emerald-600">{formatUSD(plant.savings_usd)}</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Methodology & Prices */}
              <Card className="impact-summary">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Info className="h-5 w-5 text-primary" />
                    Calculation Details
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Electricity Price</p>
                      <p className="font-semibold">${economicSimulation.marginal_price_used_usd_mwh.toFixed(2)} /MWh</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Fuel Price</p>
                      <p className="font-semibold">${economicSimulation.fuel_price_used_usd_mmbtu.toFixed(2)} /MMBtu</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Projection Period</p>
                      <p className="font-semibold">{economicSimulation.projection_days} days</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Calculated At</p>
                      <p className="font-semibold text-sm">
                        {new Date(economicSimulation.calculated_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="p-4 bg-secondary/50 rounded-xl">
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {economicSimulation.summary}
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* SPI-based Simulation Results */}
          {simulation && !loading && (
            <div ref={resultsRef}>
              {/* Comparison Cards */}
              <div className="grid gap-6 md:grid-cols-2 mb-8">
                {/* No Action Scenario */}
                <HighlightedCard variant="danger" className="comparison-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-red-100">
                        <XCircle className="h-5 w-5 text-red-600" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">Without Action</CardTitle>
                        <CardDescription>Projected outcome if no actions taken</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-5">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending Risk Level</span>
                      <RiskBadge level={simulation.no_action.ending_risk_level} size="lg" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending SPI</span>
                      <span className="text-3xl font-bold text-red-600">
                        <AnimatedCounter value={simulation.no_action.ending_spi} decimals={2} />
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Days to Critical</span>
                      <span className="text-3xl font-bold text-red-600">
                        <AnimatedCounter value={simulation.no_action.days_to_critical} />
                      </span>
                    </div>
                  </CardContent>
                </HighlightedCard>

                {/* With Action Scenario */}
                <HighlightedCard variant="success" className="comparison-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-xl bg-emerald-100">
                        <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">With Action</CardTitle>
                        <CardDescription>Projected outcome with selected actions</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-5">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending Risk Level</span>
                      <RiskBadge level={simulation.with_action.ending_risk_level} size="lg" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending SPI</span>
                      <span className="text-3xl font-bold text-emerald-600">
                        <AnimatedCounter value={simulation.with_action.ending_spi} decimals={2} />
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Days to Critical</span>
                      <span className="text-3xl font-bold text-emerald-600">
                        <AnimatedCounter value={simulation.with_action.days_to_critical} />
                      </span>
                    </div>
                  </CardContent>
                </HighlightedCard>
              </div>

              {/* Impact Summary */}
              <Card className="impact-summary mb-8 bg-gradient-to-br from-emerald-50 via-background to-blue-50 border-emerald-200">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-emerald-600" />
                    Impact Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid sm:grid-cols-3 gap-8 mb-6">
                    <div className="text-center">
                      <div className="text-5xl font-bold text-emerald-600 mb-1">
                        +<AnimatedCounter value={simulation.comparison.days_gained} />
                      </div>
                      <div className="text-sm font-medium text-muted-foreground">Days Gained</div>
                    </div>
                    <div className="text-center">
                      <div className="text-5xl font-bold text-primary mb-1">
                        +<AnimatedCounter value={simulation.comparison.spi_improvement} decimals={2} />
                      </div>
                      <div className="text-sm font-medium text-muted-foreground">SPI Improvement</div>
                    </div>
                    <div className="text-center">
                      <div className="text-5xl font-bold text-foreground mb-1">
                        <AnimatedCounter value={simulation.comparison.actions_count} />
                      </div>
                      <div className="text-sm font-medium text-muted-foreground">Actions Applied</div>
                    </div>
                  </div>
                  <div className="p-5 bg-background rounded-xl border">
                    <p className="text-sm">
                      <strong className="text-emerald-600">Result:</strong>{' '}
                      <span className="text-foreground">{simulation.comparison.risk_level_change}</span>
                    </p>
                    <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
                      {simulation.summary}
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* AI Analysis Brief for SPI Simulation */}
              {simulation.ai_brief && (
                <Card className="mb-8 border-primary/20 bg-gradient-to-br from-primary/5 to-transparent">
                  <CardHeader className="pb-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 rounded-xl bg-primary/10">
                          <Brain className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">AI Analysis</CardTitle>
                          <CardDescription>
                            {simulation.ai_brief.generated 
                              ? 'AI-generated insights and recommendations' 
                              : 'Analysis based on simulation data'}
                          </CardDescription>
                        </div>
                      </div>
                      {simulation.ai_brief.generated && (
                        <Badge variant="outline" className="text-xs">
                          <Sparkles className="h-3 w-3 mr-1" />
                          AI Generated
                        </Badge>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Executive Summary */}
                    <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                      <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        Executive Summary
                      </h4>
                      <p className="text-sm leading-relaxed">
                        {simulation.ai_brief.executive_summary}
                      </p>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2">
                      {/* Risk Context */}
                      <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                        <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                          <AlertOctagon className="h-4 w-4" />
                          Risk Context
                        </h4>
                        <p className="text-sm leading-relaxed">
                          {simulation.ai_brief.risk_context}
                        </p>
                      </div>

                      {/* Action Rationale */}
                      <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                        <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                          <Lightbulb className="h-4 w-4" />
                          Why These Actions Work
                        </h4>
                        <p className="text-sm leading-relaxed">
                          {simulation.ai_brief.action_rationale}
                        </p>
                      </div>
                    </div>

                    {/* Recommendation */}
                    <div className="p-4 rounded-xl bg-primary/5 border border-primary/10">
                      <h4 className="font-semibold text-sm text-primary mb-2 flex items-center gap-2">
                        <ArrowUpRight className="h-4 w-4" />
                        Recommendation
                      </h4>
                      <p className="text-sm leading-relaxed">
                        {simulation.ai_brief.recommendation}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Trajectory Chart */}
              <Card ref={chartRef}>
                <CardHeader>
                  <CardTitle>SPI Trajectory Comparison</CardTitle>
                  <CardDescription>
                    Projected SPI values over {projectionDays} days
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-[400px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis 
                          dataKey="day" 
                          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
                          tickLine={false}
                          axisLine={{ stroke: 'var(--border)' }}
                          label={{ value: 'Days', position: 'bottom', offset: -5, fill: 'var(--muted-foreground)' }}
                        />
                        <YAxis 
                          domain={[-3, 0]}
                          tick={{ fontSize: 12, fill: 'var(--muted-foreground)' }}
                          tickLine={false}
                          axisLine={{ stroke: 'var(--border)' }}
                          label={{ value: 'SPI', angle: -90, position: 'insideLeft', fill: 'var(--muted-foreground)' }}
                        />
                        <Tooltip 
                          content={({ active, payload, label }) => {
                            if (active && payload && payload.length) {
                              return (
                                <div className="bg-background border border-border rounded-xl p-4 shadow-lg">
                                  <p className="text-sm font-semibold mb-2">Day {label}</p>
                                  {payload.map((p, i) => (
                                    <p key={i} className="text-sm flex items-center gap-2" style={{ color: p.color }}>
                                      <span className="w-3 h-3 rounded-full" style={{ background: p.color }} />
                                      {p.name}: {Number(p.value).toFixed(2)}
                                    </p>
                                  ))}
                                </div>
                              );
                            }
                            return null;
                          }}
                        />
                        <Legend 
                          wrapperStyle={{ paddingTop: '20px' }}
                          formatter={(value) => <span className="text-sm font-medium">{value}</span>}
                        />
                        {/* Threshold lines */}
                        <ReferenceLine y={-2} stroke="#DF1B41" strokeDasharray="5 5" strokeWidth={1.5} />
                        <ReferenceLine y={-1.5} stroke="#ED5F00" strokeDasharray="5 5" strokeWidth={1.5} />
                        <Line
                          type="monotone"
                          dataKey="no_action"
                          name="Without Action"
                          stroke="#DF1B41"
                          strokeWidth={2.5}
                          dot={false}
                        />
                        <Line
                          type="monotone"
                          dataKey="with_action"
                          name="With Action"
                          stroke="#0E6245"
                          strokeWidth={2.5}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
}
