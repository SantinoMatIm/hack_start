/**
 * API Client for Water Risk Platform
 * Connects to FastAPI backend
 */

import type {
  ZoneListResponse,
  Zone,
  RiskResponse,
  RiskHistoryResponse,
  Action,
  RecommendedActionsRequest,
  RecommendedActionsResponse,
  SimulationRequest,
  SimulationResponse,
  HealthResponse,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(response.status, errorText || `HTTP ${response.status}`);
  }

  return response.json();
}

// ============ Health ============

export async function getHealth(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>('/health');
}

// ============ Zones ============

export async function getZones(): Promise<ZoneListResponse> {
  return fetchApi<ZoneListResponse>('/zones');
}

export async function getZone(zoneId: string): Promise<Zone> {
  return fetchApi<Zone>(`/zones/${zoneId}`);
}

// ============ Risk ============

export async function getCurrentRisk(zoneId: string): Promise<RiskResponse> {
  return fetchApi<RiskResponse>(`/risk/current?zone_id=${zoneId}`);
}

export async function getRiskHistory(
  zoneId: string,
  days: number = 30
): Promise<RiskHistoryResponse> {
  return fetchApi<RiskHistoryResponse>(
    `/risk/history?zone_id=${zoneId}&days=${days}`
  );
}

// ============ Actions ============

export async function getActions(): Promise<Action[]> {
  return fetchApi<Action[]>('/actions');
}

export async function getAction(actionCode: string): Promise<Action> {
  return fetchApi<Action>(`/actions/${actionCode}`);
}

export async function getRecommendedActions(
  request: RecommendedActionsRequest
): Promise<RecommendedActionsResponse> {
  return fetchApi<RecommendedActionsResponse>('/actions/recommended', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// ============ Simulation ============

export async function simulateScenario(
  request: SimulationRequest
): Promise<SimulationResponse> {
  return fetchApi<SimulationResponse>('/scenarios/simulate', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// ============ Demo Data (Fallback) ============

export const DEMO_ZONES: Zone[] = [
  {
    id: 'cdmx',
    name: 'Mexico City',
    slug: 'cdmx',
    latitude: 19.4326,
    longitude: -99.1332,
    created_at: new Date().toISOString(),
  },
  {
    id: 'monterrey',
    name: 'Monterrey',
    slug: 'monterrey',
    latitude: 25.6866,
    longitude: -100.3161,
    created_at: new Date().toISOString(),
  },
];

export const DEMO_RISK_CDMX: RiskResponse = {
  zone_id: 'cdmx',
  spi_6m: -1.72,
  risk_level: 'HIGH',
  trend: 'WORSENING',
  days_to_critical: 24,
  last_updated: new Date().toISOString(),
};

export const DEMO_RISK_MONTERREY: RiskResponse = {
  zone_id: 'monterrey',
  spi_6m: -1.45,
  risk_level: 'HIGH',
  trend: 'STABLE',
  days_to_critical: 38,
  last_updated: new Date().toISOString(),
};

export function getDemoRisk(zoneId: string): RiskResponse {
  return zoneId === 'cdmx' ? DEMO_RISK_CDMX : DEMO_RISK_MONTERREY;
}

// API Client object for convenient imports
export const api = {
  getHealth,
  getZones,
  getZone,
  getCurrentRisk,
  getRiskHistory,
  getActions,
  getAction,
  getRecommendedActions,
  simulateScenario,
  // Demo data
  DEMO_ZONES,
  getDemoRisk,
};

export default api;
