// API Types for Water Risk Platform (Energy Infrastructure Focus)

// Risk Levels
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type Trend = 'IMPROVING' | 'STABLE' | 'WORSENING';
export type Profile = 'government' | 'industry';

// ============ Power Plants ============

export type PlantType = 'thermoelectric' | 'nuclear' | 'hydroelectric';
export type WaterDependency = 'high' | 'medium' | 'low';
export type CoolingType = 'once_through' | 'recirculating' | 'dry';
export type OperationalStatus = 'active' | 'maintenance' | 'offline';

export interface PowerPlant {
  id: string;
  zone_id: string;
  name: string;
  plant_type: PlantType;
  capacity_mw: number;
  water_dependency: WaterDependency;
  cooling_type: CoolingType;
  latitude: number;
  longitude: number;
  operational_status: OperationalStatus;
  created_at: string;
}

export interface PowerPlantCreate {
  zone_id: string;
  name: string;
  plant_type: PlantType;
  capacity_mw: number;
  water_dependency?: WaterDependency;
  cooling_type?: CoolingType;
  latitude: number;
  longitude: number;
}

export interface PowerPlantListResponse {
  plants: PowerPlant[];
  total: number;
  total_capacity_mw: number;
}

// ============ Energy Prices (EIA) ============

export interface EnergyPricesResponse {
  marginal_price_usd_mwh: number;
  fuel_price_usd_mmbtu: number;
  fetched_at: string;
  source: 'eia' | 'fallback' | string;
}

export interface EnergyPriceHistoryPoint {
  period: string;
  price_usd_mwh?: number;
  price_usd_mmbtu?: number;
}

export interface EnergyPriceHistoryResponse {
  region: string;
  price_type: 'electricity' | 'fuel';
  history: EnergyPriceHistoryPoint[];
  total: number;
}

// ============ Economic Simulation ============

export interface EconomicSimulationRequest {
  zone_id: string;
  power_plant_ids?: string[];
  action_instance_ids?: string[];
  projection_days?: number;
}

export interface EconomicScenarioResult {
  capacity_loss_pct: number;
  total_cost_usd: number;
  emergency_fuel_cost_usd: number;
  lost_generation_mwh: number;
}

export interface PlantBreakdown {
  plant_id: string;
  plant_name: string;
  capacity_mw: number;
  no_action_cost_usd: number;
  with_action_cost_usd: number;
  savings_usd: number;
  capacity_loss_no_action: number;
  capacity_loss_with_action: number;
}

export interface AIBrief {
  executive_summary: string;
  risk_context: string;
  action_rationale: string;
  recommendation: string;
  generated: boolean;  // true if AI-generated, false if fallback
}

export interface EconomicSimulationResponse {
  zone_id: string;
  plants_analyzed: number;
  total_capacity_mw: number;
  no_action: EconomicScenarioResult;
  with_action: EconomicScenarioResult;
  savings_usd: number;
  savings_pct: number;
  summary: string;
  ai_brief?: AIBrief;  // Optional AI-generated analysis
  per_plant_breakdown: PlantBreakdown[];
  marginal_price_used_usd_mwh: number;
  fuel_price_used_usd_mmbtu: number;
  projection_days: number;
  calculated_at: string;
}

// ============ Zone (Extended) ============

export interface Zone {
  id: string;
  name: string;
  slug: string;
  latitude: number;
  longitude: number;
  // Energy pricing fields
  energy_price_usd_mwh?: number;
  fuel_price_usd_mmbtu?: number;
  currency?: string;
  // Regional codes (for EIA/NOAA)
  country_code?: string;
  state_code?: string;
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

export interface SPIBrief {
  executive_summary: string;
  risk_context: string;
  action_rationale: string;
  recommendation: string;
  generated: boolean;  // true if AI-generated, false if fallback
}

export interface SimulationResponse {
  zone_id: string;
  no_action: ScenarioResult;
  with_action: ScenarioResult;
  comparison: ScenarioComparison;
  summary: string;
  ai_brief?: SPIBrief;  // Optional AI-generated analysis
  actions_applied: ActionApplied[];
}

// Health
export interface HealthResponse {
  status: string;
  environment: string;
  demo_mode: boolean;
  database_configured: boolean;
  openai_configured: boolean;
  eia_configured?: boolean;
  note?: string;
}
