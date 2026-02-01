/**
 * API Client for Water Risk Platform
 * Energy Infrastructure Focus - Connects to FastAPI backend
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
  // Energy/Economic types
  EnergyPricesResponse,
  EnergyPriceHistoryResponse,
  EconomicSimulationRequest,
  EconomicSimulationResponse,
  PowerPlant,
  PowerPlantCreate,
  PowerPlantListResponse,
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

// Request queue to prevent overwhelming Supabase's connection limits
// Serializes requests with a small delay between them
class RequestQueue {
  private queue: Array<() => Promise<void>> = [];
  private processing = false;
  private lastRequestTime = 0;
  private minDelayMs = 100; // Minimum 100ms between requests

  async add<T>(requestFn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        // Ensure minimum delay between requests
        const now = Date.now();
        const timeSinceLastRequest = now - this.lastRequestTime;
        if (timeSinceLastRequest < this.minDelayMs) {
          await new Promise(r => setTimeout(r, this.minDelayMs - timeSinceLastRequest));
        }
        
        try {
          const result = await requestFn();
          this.lastRequestTime = Date.now();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      });
      
      this.processQueue();
    });
  }

  private async processQueue() {
    if (this.processing || this.queue.length === 0) return;
    
    this.processing = true;
    while (this.queue.length > 0) {
      const task = this.queue.shift();
      if (task) {
        await task();
      }
    }
    this.processing = false;
  }
}

const requestQueue = new RequestQueue();

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  return requestQueue.add(async () => {
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
  });
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

// ============ Economic / EIA ============

export async function getEnergyPrices(region: string = "US"): Promise<EnergyPricesResponse> {
  return fetchApi<EnergyPricesResponse>(`/economic/prices?region=${region}`);
}

export async function getEnergyPriceHistory(
  region: string = "US",
  priceType: 'electricity' | 'fuel' = "electricity",
  days: number = 30
): Promise<EnergyPriceHistoryResponse> {
  return fetchApi<EnergyPriceHistoryResponse>(
    `/economic/prices/history?region=${region}&price_type=${priceType}&days=${days}`
  );
}

export async function runEconomicSimulation(
  request: EconomicSimulationRequest
): Promise<EconomicSimulationResponse> {
  return fetchApi<EconomicSimulationResponse>('/economic/simulate', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// ============ Power Plants ============

export async function getPowerPlants(zoneId?: string): Promise<PowerPlantListResponse> {
  const params = zoneId ? `?zone_id=${zoneId}` : '';
  return fetchApi<PowerPlantListResponse>(`/plants${params}`);
}

export async function getPowerPlant(plantId: string): Promise<PowerPlant> {
  return fetchApi<PowerPlant>(`/plants/${plantId}`);
}

export async function createPowerPlant(data: PowerPlantCreate): Promise<PowerPlant> {
  return fetchApi<PowerPlant>('/plants', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updatePowerPlant(
  plantId: string,
  data: Partial<PowerPlantCreate>
): Promise<PowerPlant> {
  return fetchApi<PowerPlant>(`/plants/${plantId}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function deletePowerPlant(plantId: string): Promise<void> {
  await fetch(`${API_BASE_URL}/plants/${plantId}`, { method: 'DELETE' });
}

// ============ Zone Extensions ============

export async function updateZoneEnergyPrices(
  zoneId: string,
  data: { energy_price_usd_mwh?: number; fuel_price_usd_mmbtu?: number; currency?: string }
): Promise<Zone> {
  return fetchApi<Zone>(`/zones/${zoneId}/energy-prices`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

export async function updateZoneRegionalCodes(
  zoneId: string,
  data: { country_code?: string; state_code?: string }
): Promise<Zone> {
  return fetchApi<Zone>(`/zones/${zoneId}/regional-codes`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  });
}

// ============ Demo Data (Fallback) ============

export const DEMO_ZONES: Zone[] = [
  {
    id: 'texas',
    name: 'Texas Power Region',
    slug: 'texas',
    latitude: 31.9686,
    longitude: -99.9018,
    country_code: 'USA',
    state_code: 'TX',
    energy_price_usd_mwh: 95.0,
    fuel_price_usd_mmbtu: 3.2,
    currency: 'USD',
    created_at: new Date().toISOString(),
  },
  {
    id: 'cdmx',
    name: 'Mexico City',
    slug: 'cdmx',
    latitude: 19.4326,
    longitude: -99.1332,
    country_code: 'MEX',
    created_at: new Date().toISOString(),
  },
  {
    id: 'monterrey',
    name: 'Monterrey',
    slug: 'monterrey',
    latitude: 25.6866,
    longitude: -100.3161,
    country_code: 'MEX',
    created_at: new Date().toISOString(),
  },
];

export const DEMO_POWER_PLANTS: PowerPlant[] = [
  {
    id: 'plant-1',
    zone_id: 'texas',
    name: 'Comanche Peak Nuclear',
    plant_type: 'nuclear',
    capacity_mw: 2400,
    water_dependency: 'high',
    cooling_type: 'recirculating',
    latitude: 32.2987,
    longitude: -97.7853,
    operational_status: 'active',
    created_at: new Date().toISOString(),
  },
  {
    id: 'plant-2',
    zone_id: 'texas',
    name: 'Martin Lake Steam',
    plant_type: 'thermoelectric',
    capacity_mw: 2250,
    water_dependency: 'high',
    cooling_type: 'once_through',
    latitude: 32.2606,
    longitude: -94.5704,
    operational_status: 'active',
    created_at: new Date().toISOString(),
  },
  {
    id: 'plant-3',
    zone_id: 'texas',
    name: 'W.A. Parish Generating',
    plant_type: 'thermoelectric',
    capacity_mw: 3653,
    water_dependency: 'medium',
    cooling_type: 'recirculating',
    latitude: 29.4843,
    longitude: -95.6283,
    operational_status: 'active',
    created_at: new Date().toISOString(),
  },
];

export const DEMO_ENERGY_PRICES: EnergyPricesResponse = {
  marginal_price_usd_mwh: 95.0,
  fuel_price_usd_mmbtu: 3.2,
  fetched_at: new Date().toISOString(),
  source: 'fallback',
};

export const DEMO_ECONOMIC_SIMULATION: EconomicSimulationResponse = {
  zone_id: 'texas',
  plants_analyzed: 3,
  total_capacity_mw: 8303,
  no_action: {
    capacity_loss_pct: 0.15,
    total_cost_usd: 2850000,
    emergency_fuel_cost_usd: 150000,
    lost_generation_mwh: 30000,
  },
  with_action: {
    capacity_loss_pct: 0.05,
    total_cost_usd: 950000,
    emergency_fuel_cost_usd: 50000,
    lost_generation_mwh: 10000,
  },
  savings_usd: 1900000,
  savings_pct: 0.67,
  summary: 'Implementing water conservation actions across 3 power plants could save an estimated $1.9M over the projection period by reducing capacity loss from 15% to 5%.',
  per_plant_breakdown: [
    {
      plant_id: 'plant-1',
      plant_name: 'Comanche Peak Nuclear',
      capacity_mw: 2400,
      no_action_cost_usd: 1140000,
      with_action_cost_usd: 380000,
      savings_usd: 760000,
      capacity_loss_no_action: 0.18,
      capacity_loss_with_action: 0.06,
    },
    {
      plant_id: 'plant-2',
      plant_name: 'Martin Lake Steam',
      capacity_mw: 2250,
      no_action_cost_usd: 1068000,
      with_action_cost_usd: 356000,
      savings_usd: 712000,
      capacity_loss_no_action: 0.20,
      capacity_loss_with_action: 0.07,
    },
    {
      plant_id: 'plant-3',
      plant_name: 'W.A. Parish Generating',
      capacity_mw: 3653,
      no_action_cost_usd: 642000,
      with_action_cost_usd: 214000,
      savings_usd: 428000,
      capacity_loss_no_action: 0.10,
      capacity_loss_with_action: 0.03,
    },
  ],
  marginal_price_used_usd_mwh: 95,
  fuel_price_used_usd_mmbtu: 3.2,
  projection_days: 90,
  calculated_at: new Date().toISOString(),
};

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
  // Texas is the primary energy infrastructure zone
  if (zoneId === 'texas') {
    return {
      zone_id: 'texas',
      spi_6m: -1.55,
      risk_level: 'HIGH',
      trend: 'WORSENING',
      days_to_critical: 32,
      last_updated: new Date().toISOString(),
    };
  }
  return zoneId === 'cdmx' ? DEMO_RISK_CDMX : DEMO_RISK_MONTERREY;
}

export function getDemoEconomicSimulation(zoneId: string): EconomicSimulationResponse {
  return {
    ...DEMO_ECONOMIC_SIMULATION,
    zone_id: zoneId,
  };
}

export function getDemoPowerPlants(zoneId?: string): PowerPlantListResponse {
  const plants = zoneId 
    ? DEMO_POWER_PLANTS.filter(p => p.zone_id === zoneId)
    : DEMO_POWER_PLANTS;
  return {
    plants,
    total: plants.length,
    total_capacity_mw: plants.reduce((sum, p) => sum + p.capacity_mw, 0),
  };
}

// API Client object for convenient imports
export const api = {
  // Health
  getHealth,
  // Zones
  getZones,
  getZone,
  updateZoneEnergyPrices,
  updateZoneRegionalCodes,
  // Risk
  getCurrentRisk,
  getRiskHistory,
  // Actions
  getActions,
  getAction,
  getRecommendedActions,
  // Simulation (SPI-based)
  simulateScenario,
  // Economic simulation (USD-based)
  getEnergyPrices,
  getEnergyPriceHistory,
  runEconomicSimulation,
  // Power plants
  getPowerPlants,
  getPowerPlant,
  createPowerPlant,
  updatePowerPlant,
  deletePowerPlant,
  // Demo data
  DEMO_ZONES,
  DEMO_POWER_PLANTS,
  DEMO_ENERGY_PRICES,
  DEMO_ECONOMIC_SIMULATION,
  getDemoRisk,
  getDemoEconomicSimulation,
  getDemoPowerPlants,
};

export default api;
