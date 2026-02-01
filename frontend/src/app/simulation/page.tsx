'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { RiskBadge } from '@/components/risk-badge';
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
  ChevronLeft
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
};

export default function SimulationPage() {
  const [selectedActions, setSelectedActions] = useState<string[]>([]);
  const [selectedZone, setSelectedZone] = useState<string>('cdmx');
  const [projectionDays, setProjectionDays] = useState<number>(90);
  const [simulation, setSimulation] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    // Load selected actions from localStorage
    const storedActions = localStorage.getItem('selectedActions');
    const storedZone = localStorage.getItem('selectedZone');
    
    if (storedActions) {
      setSelectedActions(JSON.parse(storedActions));
    }
    if (storedZone) {
      setSelectedZone(storedZone);
    }
  }, []);

  const runSimulation = async () => {
    if (selectedActions.length === 0) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const data = await api.simulateScenario({
        zone_id: selectedZone,
        action_codes: selectedActions,
        projection_days: projectionDays,
      });
      setSimulation(data);
      setIsDemo(false);
    } catch (err) {
      console.warn('API unavailable, using demo data:', err);
      setSimulation(DEMO_SIMULATION);
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
    <div className="container py-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Link href="/actions">
              <Button variant="ghost" size="sm" className="gap-1">
                <ChevronLeft className="h-4 w-4" />
                Back to Actions
              </Button>
            </Link>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Scenario Simulation</h1>
          <p className="text-muted-foreground mt-1">
            Compare outcomes: Act vs. Not Act
          </p>
        </div>
      </div>

      {/* Demo Mode Alert */}
      {isDemo && (
        <Alert className="mb-6">
          <Info className="h-4 w-4" />
          <AlertTitle>Demo Mode</AlertTitle>
          <AlertDescription>
            Showing simulated projections. Connect to API for actual calculations.
          </AlertDescription>
        </Alert>
      )}

      {/* No Actions Selected */}
      {selectedActions.length === 0 ? (
        <Card className="border-dashed">
          <CardContent className="py-12 text-center">
            <AlertTriangle className="h-12 w-12 text-amber-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No Actions Selected</h3>
            <p className="text-muted-foreground mb-4">
              Select actions from the Actions page to run a simulation.
            </p>
            <Button asChild>
              <Link href="/actions">
                Go to Actions
                <ArrowRight className="h-4 w-4 ml-2" />
              </Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Selected Actions Summary */}
          <Card className="mb-6">
            <CardHeader className="pb-3">
              <CardTitle className="text-base">Simulation Parameters</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Zone:</span>
                  <Badge variant="outline">{zoneName}</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Actions:</span>
                  {selectedActions.map(code => (
                    <Badge key={code} variant="secondary">{code}</Badge>
                  ))}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-muted-foreground">Projection:</span>
                  <span className="font-medium">{projectionDays} days</span>
                </div>
                <div className="ml-auto">
                  <Button onClick={runSimulation} disabled={loading} className="gap-2">
                    {loading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Play className="h-4 w-4" />
                    )}
                    {loading ? 'Simulating...' : 'Run Simulation'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Loading State */}
          {loading && (
            <div className="grid gap-6 md:grid-cols-2">
              {[...Array(2)].map((_, i) => (
                <Card key={i}>
                  <CardHeader>
                    <Skeleton className="h-5 w-1/2" />
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Skeleton className="h-8 w-24" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Simulation Results */}
          {simulation && !loading && (
            <>
              {/* Comparison Cards */}
              <div className="grid gap-6 md:grid-cols-2 mb-8">
                {/* No Action Scenario */}
                <Card className="border-red-200 dark:border-red-900">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <XCircle className="h-5 w-5 text-red-500" />
                      <CardTitle className="text-lg">Without Action</CardTitle>
                    </div>
                    <CardDescription>Projected outcome if no actions are taken</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending Risk Level</span>
                      <RiskBadge level={simulation.no_action.ending_risk_level} size="lg" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending SPI</span>
                      <span className="text-2xl font-bold text-red-600 dark:text-red-400">
                        {simulation.no_action.ending_spi.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Days to Critical</span>
                      <span className="text-2xl font-bold text-red-600 dark:text-red-400">
                        {simulation.no_action.days_to_critical}
                      </span>
                    </div>
                  </CardContent>
                </Card>

                {/* With Action Scenario */}
                <Card className="border-emerald-200 dark:border-emerald-900">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-5 w-5 text-emerald-500" />
                      <CardTitle className="text-lg">With Action</CardTitle>
                    </div>
                    <CardDescription>Projected outcome with selected actions</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending Risk Level</span>
                      <RiskBadge level={simulation.with_action.ending_risk_level} size="lg" />
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Ending SPI</span>
                      <span className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                        {simulation.with_action.ending_spi.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Days to Critical</span>
                      <span className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">
                        {simulation.with_action.days_to_critical}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Impact Summary */}
              <Card className="mb-8 bg-gradient-to-r from-emerald-50 to-blue-50 dark:from-emerald-950/30 dark:to-blue-950/30 border-emerald-200 dark:border-emerald-900">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-emerald-600" />
                    Impact Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid sm:grid-cols-3 gap-6">
                    <div className="text-center">
                      <div className="text-4xl font-bold text-emerald-600 dark:text-emerald-400">
                        +{simulation.comparison.days_gained}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">Days Gained</div>
                    </div>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-blue-600 dark:text-blue-400">
                        +{simulation.comparison.spi_improvement.toFixed(2)}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">SPI Improvement</div>
                    </div>
                    <div className="text-center">
                      <div className="text-4xl font-bold text-primary">
                        {simulation.comparison.actions_count}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">Actions Applied</div>
                    </div>
                  </div>
                  <div className="mt-6 p-4 bg-background rounded-lg">
                    <p className="text-sm">
                      <strong>Result:</strong> {simulation.comparison.risk_level_change}
                    </p>
                    <p className="text-sm text-muted-foreground mt-2">
                      {simulation.summary}
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Trajectory Chart */}
              <Card>
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
                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                        <XAxis 
                          dataKey="day" 
                          tick={{ fontSize: 12 }}
                          tickLine={false}
                          label={{ value: 'Days', position: 'bottom', offset: -5 }}
                        />
                        <YAxis 
                          domain={[-3, 0]}
                          tick={{ fontSize: 12 }}
                          tickLine={false}
                          label={{ value: 'SPI', angle: -90, position: 'insideLeft' }}
                        />
                        <Tooltip 
                          content={({ active, payload, label }) => {
                            if (active && payload && payload.length) {
                              return (
                                <div className="bg-background border rounded-lg p-3 shadow-lg">
                                  <p className="text-sm font-medium mb-2">Day {label}</p>
                                  {payload.map((p, i) => (
                                    <p key={i} className="text-sm" style={{ color: p.color }}>
                                      {p.name}: {Number(p.value).toFixed(2)}
                                    </p>
                                  ))}
                                </div>
                              );
                            }
                            return null;
                          }}
                        />
                        <Legend />
                        {/* Threshold lines */}
                        <ReferenceLine y={-2} stroke="#DC2626" strokeDasharray="5 5" />
                        <ReferenceLine y={-1.5} stroke="#EA580C" strokeDasharray="5 5" />
                        <Line
                          type="monotone"
                          dataKey="no_action"
                          name="Without Action"
                          stroke="#DC2626"
                          strokeWidth={2}
                          dot={false}
                        />
                        <Line
                          type="monotone"
                          dataKey="with_action"
                          name="With Action"
                          stroke="#059669"
                          strokeWidth={2}
                          dot={false}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </>
      )}
    </div>
  );
}
