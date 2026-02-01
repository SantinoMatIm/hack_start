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
  Target
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

export default function SimulationPage() {
  const [selectedActions, setSelectedActions] = useState<StoredAction[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('cdmx');
  const [projectionDays, setProjectionDays] = useState<number>(90);
  const [simulation, setSimulation] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  const resultsRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<HTMLDivElement>(null);

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
    if (prefersReducedMotion() || loading || !simulation) return;

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
  }, { dependencies: [loading, simulation] });

  const runSimulation = async () => {
    if (selectedActions.length === 0) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.simulateScenario({
        zone_id: selectedZone,
        action_instance_ids: selectedActions.map(a => a.action_instance_id),
        projection_days: projectionDays,
      });
      setSimulation(data);
      setIsDemo(false);
    } catch (err) {
      console.warn('API unavailable, using demo data:', err);
      // Update demo simulation with selected actions info
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
      setIsDemo(true);
    } finally {
      setLoading(false);
    }
  };

  // Prepare chart data
  const chartData = simulation ? simulation.no_action.trajectory.map((point, i) => ({
    day: point.day,
    no_action: point.projected_spi,
    with_action: simulation.with_action.trajectory[i]?.projected_spi,
  })) : [];

  const zoneName = DEMO_ZONES.find(z => z.slug === selectedZone)?.name || selectedZone;

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
            Scenario Analysis
          </span>
          <h1 className="text-3xl font-bold tracking-tight">Simulation</h1>
          <p className="text-muted-foreground mt-1">
            Compare outcomes: Act vs. Not Act
          </p>
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

      {/* No Actions Selected */}
      {selectedActions.length === 0 ? (
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
                Select actions from the Actions page to run a simulation and see projected outcomes.
              </p>
              <Button asChild size="lg">
                <Link href="/actions">
                  Go to Actions
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Link>
              </Button>
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
                    <span className="text-sm text-muted-foreground">Actions:</span>
                    <div className="flex gap-1 flex-wrap">
                      {selectedActions.map(action => (
                        <Badge key={action.action_instance_id} variant="secondary" className="text-xs">{action.action_code}</Badge>
                      ))}
                    </div>
                  </div>
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
                      {loading ? 'Simulating...' : 'Run Simulation'}
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

          {/* Simulation Results */}
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
