// API Types for Water Risk Platform

// Risk Levels
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type Trend = 'IMPROVING' | 'STABLE' | 'WORSENING';
export type Profile = 'government' | 'industry';

// Zone
export interface Zone {
  id: string;
  name: string;
  slug: string;
  latitude: number;
  longitude: number;
  created_at: string;
}

export interface ZoneListResponse {
  zones: Zone[];
  total: number;
}

// Risk Assessment
export interface RiskResponse {
  zone_id: string;
  spi_6m: number;
  risk_level: RiskLevel;
  trend: Trend;
  days_to_critical: number;
  trend_details?: {
    short_term: Trend;
    long_term: Trend;
    velocity: number;
  };
  last_updated: string;
}

export interface RiskSnapshot {
  id: string;
  spi_6m: number;
  risk_level: RiskLevel;
  trend: Trend;
  days_to_critical: number;
  created_at: string;
}

export interface RiskHistoryResponse {
  zone_id: string;
  snapshots: RiskSnapshot[];
  total: number;
}

// Actions
export interface Action {
  id: string;
  code: string;
  title: string;
  description: string;
  heuristic: string;
  spi_min: number;
  spi_max: number;
  impact_formula: string;
  base_cost: number;
  default_urgency_days: number;
  parameter_schema: Record<string, unknown>;
}

export interface ExpectedEffect {
  days_gained: number;
  confidence: 'high' | 'medium' | 'low' | 'estimated';
  formula: string;
}

export interface RecommendedAction {
  action_instance_id: string;  // UUID for simulation
  action_code: string;
  title: string;
  description: string;
  heuristic_id: string;
  priority_score: number;
  parameters: Record<string, unknown>;
  justification: string;
  expected_effect: ExpectedEffect;
  method: 'ai' | 'fallback' | 'demo';
}

export interface ContextSummary {
  spi: number;
  risk_level: RiskLevel;
  trend: Trend;
  days_to_critical: number;
  profile: Profile;
  zone: string;
}

export interface ActivatedHeuristic {
  id: string;
  priority: number;
  actions_count: number;
}

export interface RecommendedActionsRequest {
  zone_id: string;
  profile: Profile;
}

export interface RecommendedActionsResponse {
  zone_id: string;
  profile: Profile;
  context: ContextSummary;
  activated_heuristics: ActivatedHeuristic[];
  actions: RecommendedAction[];
}

// Simulation
export interface TrajectoryPoint {
  day: number;
  projected_spi: number;
  risk_level: RiskLevel;
  improvement_applied: boolean;
}

export interface ScenarioResult {
  ending_spi: number;
  ending_risk_level: RiskLevel;
  days_to_critical: number;
  trajectory: TrajectoryPoint[];
}

export interface ScenarioComparison {
  days_gained: number;
  spi_improvement: number;
  risk_level_change: string;
  actions_count: number;
}

export interface SimulationRequest {
  zone_id: string;
  action_instance_ids: string[];  // UUIDs from RecommendedAction
  projection_days?: number;
}

export interface ActionApplied {
  code: string;
  title: string;
  days_gained: number;
}

export interface SimulationResponse {
  zone_id: string;
  no_action: ScenarioResult;
  with_action: ScenarioResult;
  comparison: ScenarioComparison;
  summary: string;
  actions_applied: ActionApplied[];
}

// Health
export interface HealthResponse {
  status: string;
  environment: string;
  demo_mode: boolean;
  database_configured: boolean;
  openai_configured: boolean;
  note?: string;
}
