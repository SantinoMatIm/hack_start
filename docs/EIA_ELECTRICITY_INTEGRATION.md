# Integración EIA y enfoque en electricidad

Documentación de la integración con la API de EIA (Energy Information Administration) y el enfoque especializado en infraestructura eléctrica para la plataforma Water Risk.

---

## 1. Resumen ejecutivo

La integración EIA añade:
- **Precios de electricidad** (retail, USD/MWh) por región/estado
- **Precios de gas natural** (spot, USD/MMBtu) para costos de emergencia
- **Simulación económica** de impacto del estrés hídrico en plantas eléctricas
- **Modelo de power plants** (plantas termoeléctricas, nucleares, hidroeléctricas)

---

## 2. Configuración

### 2.1 Variables de entorno

| Variable | Descripción | Obligatorio |
|----------|-------------|-------------|
| `EIA_API_KEY` | API key de EIA Open Data (https://www.eia.gov/opendata/) | Sí, para precios en vivo |

### 2.2 Verificación

```
GET /health
```

Respuesta incluye `eia_configured: true/false`.

---

## 3. API EIA – datos utilizados

### 3.1 Fuentes EIA

| Endpoint EIA | Datos | Unidades | Uso |
|--------------|-------|----------|-----|
| `/electricity/retail-sales/data` | Precio retail electricidad | cents/kWh → USD/MWh (×10) | P_marginal para costos de generación perdida |
| `/natural-gas/pri/fut/data` | Precio spot gas natural (Henry Hub) | USD/MMBtu | Costos de emergencia / combustible de respaldo |

### 3.2 Parámetros electricidad

- **state**: código estado US (TX, CA, AZ) o `null` para promedio nacional
- **sector**: ALL, RES, COM, IND
- **length**: últimos 12 meses

### 3.3 Conversión unidades

- EIA devuelve electricidad en **cents/kWh**
- Conversión: `1 cent/kWh = 10 USD/MWh`

---

## 4. Endpoints API – catálogo completo

### 4.1 Economic (nuevo)

**Base path:** `/economic`

#### GET /economic/prices

Precios actuales de energía desde EIA.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `region` | query | US | Región (US, TX, CA, etc.) |

**Respuesta 200:**
```json
{
  "marginal_price_usd_mwh": 100.0,
  "fuel_price_usd_mmbtu": 3.0,
  "fetched_at": "2026-02-01T12:00:00",
  "source": "eia"
}
```

- `source`: "eia" | "fallback" | "fallback (EIA error: ...)"

---

#### GET /economic/prices/history

Histórico de precios para análisis de tendencias.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `region` | query | US | Región (US, TX, CA) |
| `price_type` | query | electricity | "electricity" o "fuel" |
| `days` | query | 30 | Días de histórico (1–365) |

**Respuesta 200:**
```json
{
  "region": "TX",
  "price_type": "electricity",
  "history": [
    {"period": "2025-01", "price_usd_mwh": 95.2, "price_usd_mmbtu": null},
    {"period": "2025-02", "price_usd_mwh": 102.1, "price_usd_mmbtu": null}
  ],
  "total": 12
}
```

- Electricidad: `price_usd_mwh`
- Gas: `price_usd_mmbtu`

---

#### POST /economic/simulate

Simulación de impacto económico del estrés hídrico en plantas eléctricas.

**Request body:**
```json
{
  "zone_id": "texas",
  "power_plant_ids": [],
  "action_instance_ids": [],
  "projection_days": 90
}
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `zone_id` | string | Slug o UUID de la zona |
| `power_plant_ids` | string[] | UUIDs de plantas. Vacío = todas las plantas de la zona |
| `action_instance_ids` | string[] | UUIDs de acciones. Vacío = mejora SPI estimada 0.3 |
| `projection_days` | int | Días de proyección (1–365) |

**Respuesta 200:**
```json
{
  "zone_id": "texas",
  "plants_analyzed": 5,
  "total_capacity_mw": 2500,
  "no_action": {
    "capacity_loss_pct": 0.15,
    "total_cost_usd": 450000,
    "emergency_fuel_cost_usd": 0,
    "lost_generation_mwh": 4500
  },
  "with_action": {
    "capacity_loss_pct": 0.05,
    "total_cost_usd": 150000,
    "emergency_fuel_cost_usd": 0,
    "lost_generation_mwh": 1500
  },
  "savings_usd": 300000,
  "savings_pct": 0.67,
  "summary": "Implementing water actions across 5 power plants...",
  "per_plant_breakdown": [
    {
      "plant_id": "uuid",
      "plant_name": "Plant A",
      "capacity_mw": 500,
      "no_action_cost_usd": 90000,
      "with_action_cost_usd": 30000,
      "savings_usd": 60000,
      "capacity_loss_no_action": 0.15,
      "capacity_loss_with_action": 0.05
    }
  ],
  "marginal_price_used_usd_mwh": 100,
  "fuel_price_used_usd_mmbtu": 3,
  "projection_days": 90,
  "calculated_at": "2026-02-01T12:00:00"
}
```

**Prioridad de precios:**
1. Precios de zona (`zones.energy_price_usd_mwh`)
2. EIA API (por `zone.state_code` si USA)
3. Fallback: 100 USD/MWh, 3 USD/MMBtu

---

### 4.2 Power Plants (nuevo)

**Base path:** `/plants`

#### GET /plants

Listar plantas eléctricas.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `zone_id` | query | Filtrar por zona (slug o UUID) |

**Respuesta 200:**
```json
{
  "plants": [
    {
      "id": "uuid",
      "zone_id": "uuid",
      "name": "Plant A",
      "plant_type": "thermoelectric",
      "capacity_mw": 500,
      "water_dependency": "high",
      "cooling_type": "recirculating",
      "latitude": 31.96,
      "longitude": -99.90,
      "operational_status": "active",
      "created_at": "2026-02-01T12:00:00"
    }
  ],
  "total": 5,
  "total_capacity_mw": 2500
}
```

---

#### POST /plants

Crear planta eléctrica.

**Request body:**
```json
{
  "zone_id": "texas",
  "name": "Plant A",
  "plant_type": "thermoelectric",
  "capacity_mw": 500,
  "water_dependency": "high",
  "cooling_type": "recirculating",
  "latitude": 31.9686,
  "longitude": -99.9018
}
```

| Campo | Tipo | Valores | Descripción |
|-------|------|---------|-------------|
| `plant_type` | string | thermoelectric, nuclear, hydroelectric | Tipo de planta |
| `water_dependency` | string | high, medium, low | Dependencia hídrica |
| `cooling_type` | string | once_through, recirculating, dry | Tipo de enfriamiento |

**Respuesta 201:** objeto planta creada

---

#### GET /plants/{plant_id}

Detalle de una planta.

---

#### PATCH /plants/{plant_id}

Actualizar planta.

**Campos opcionales:** `name`, `plant_type`, `capacity_mw`, `water_dependency`, `cooling_type`, `operational_status` (active, maintenance, offline), `latitude`, `longitude`

---

#### DELETE /plants/{plant_id}

Eliminar planta. **204 No Content**

---

### 4.3 Zones – cambios

#### POST /zones (ampliado)

**Campos nuevos:**

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `country_code` | string | ISO 3166-1 alpha-3 (USA, MEX, SOM) |
| `state_code` | string | Código estado US (TX, CA, AZ) |

**Ejemplo:**
```json
{
  "name": "Texas Power Region",
  "slug": "texas",
  "latitude": 31.9686,
  "longitude": -99.9018,
  "country_code": "USA",
  "state_code": "TX"
}
```

---

#### PATCH /zones/{zone_id}/energy-prices (nuevo)

Actualizar precios locales de energía.

**Request body:**
```json
{
  "energy_price_usd_mwh": 95.0,
  "fuel_price_usd_mmbtu": 3.5,
  "currency": "USD"
}
```

---

#### PATCH /zones/{zone_id}/regional-codes (nuevo)

Actualizar códigos regionales (NOAA, EIA).

**Request body:**
```json
{
  "country_code": "USA",
  "state_code": "TX"
}
```

---

#### GET /zones – respuesta ampliada

Cada zona incluye:

```json
{
  "id": "...",
  "name": "Texas Power Region",
  "slug": "texas",
  "latitude": 31.96,
  "longitude": -99.90,
  "energy_price_usd_mwh": null,
  "fuel_price_usd_mmbtu": null,
  "currency": "USD",
  "country_code": "USA",
  "state_code": "TX",
  "created_at": "..."
}
```

---

## 5. Modelo de datos

### 5.1 Tablas nuevas (migraciones 002–004)

| Tabla | Descripción |
|-------|-------------|
| `power_plants` | Plantas eléctricas por zona |
| `energy_price_cache` | Cache de precios EIA (no usada aún en endpoints) |
| `economic_simulations` | Resultados de simulación económica |

### 5.2 Columnas nuevas en `zones`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `energy_price_usd_mwh` | float | Precio local electricidad |
| `fuel_price_usd_mmbtu` | float | Precio local gas |
| `currency` | string | Moneda (default USD) |
| `country_code` | string | País (USA, MEX) |
| `state_code` | string | Estado US (TX, CA) |

### 5.3 PowerPlant

| Campo | Tipo | Valores |
|-------|------|---------|
| plant_type | string | thermoelectric, nuclear, hydroelectric |
| water_dependency | string | high, medium, low |
| cooling_type | string | once_through, recirculating, dry |
| operational_status | string | active, maintenance, offline |

---

## 6. Integración en frontend

### 6.1 Frontend TypeScript – `frontend/src/lib/api/client.ts`

Añadir al objeto `api` y exportar:

```typescript
// ============ Economic / EIA ============

export async function getEnergyPrices(region: string = "US"): Promise<EnergyPricesResponse> {
  return fetchApi<EnergyPricesResponse>(`/economic/prices?region=${region}`);
}

export async function getEnergyPriceHistory(
  region: string = "US",
  priceType: string = "electricity",
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
```

---

### 6.2 Páginas/sections sugeridas

| Sección | Descripción | Endpoints |
|---------|-------------|-----------|
| Precios energía | Tarjeta con precios actuales y mini gráfico histórico | GET /economic/prices, /economic/prices/history |
| Plantas eléctricas | CRUD de plantas por zona, tabla con capacidad total | GET/POST/PATCH/DELETE /plants |
| Simulación económica | Formulario zone + plantas + proyección → resultados | POST /economic/simulate |
| Config zona | Formulario para precios y códigos regionales | PATCH /zones/{id}/energy-prices, /regional-codes |

---

### 6.2 Frontend TypeScript – `frontend/src/lib/api/types.ts`

Añadir tipos e interfaces.

---

### 6.3 Flujo típico en el front

1. **Zonas US:** crear/editar con `country_code: "USA"` y `state_code` (TX, CA, etc.).
2. **Plantas:** listar por zona, crear con `zone_id`, tipo y capacidad.
3. **Precios:** mostrar precios actuales; opcional: histórico.
4. **Simulación económica:**
   - Seleccionar zona (con plantas).
   - Opcional: acciones recomendadas.
   - Ejecutar simulación.
   - Mostrar savings, breakdown por planta, summary.

---

### 6.4 Tipos / interfaces (TypeScript) – `frontend/src/lib/api/types.ts`

```typescript
// Energy prices (EIA)
export interface EnergyPricesResponse {
  marginal_price_usd_mwh: number;
  fuel_price_usd_mmbtu: number;
  fetched_at: string;
  source: string;
}

export interface EnergyPriceHistoryPoint {
  period: string;
  price_usd_mwh?: number;
  price_usd_mmbtu?: number;
}

export interface EnergyPriceHistoryResponse {
  region: string;
  price_type: string;
  history: EnergyPriceHistoryPoint[];
  total: number;
}

// Power plant
export type PlantType = 'thermoelectric' | 'nuclear' | 'hydroelectric';
export type WaterDependency = 'high' | 'medium' | 'low';
export type OperationalStatus = 'active' | 'maintenance' | 'offline';

export interface PowerPlant {
  id: string;
  zone_id: string;
  name: string;
  plant_type: PlantType;
  capacity_mw: number;
  water_dependency: WaterDependency;
  cooling_type: string;
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
  cooling_type?: string;
  latitude: number;
  longitude: number;
}

export interface PowerPlantListResponse {
  plants: PowerPlant[];
  total: number;
  total_capacity_mw: number;
}

// Economic simulation
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

export interface EconomicSimulationResponse {
  zone_id: string;
  plants_analyzed: number;
  total_capacity_mw: number;
  no_action: EconomicScenarioResult;
  with_action: EconomicScenarioResult;
  savings_usd: number;
  savings_pct: number;
  summary: string;
  per_plant_breakdown: PlantBreakdown[];
  marginal_price_used_usd_mwh: number;
  fuel_price_used_usd_mmbtu: number;
  projection_days: number;
  calculated_at: string;
}

// Zone (extended) - add to existing Zone interface
// energy_price_usd_mwh?: number;
// fuel_price_usd_mmbtu?: number;
// currency?: string;
// country_code?: string;
// state_code?: string;
```

---

## 7. Lógica económica (backend)

### 7.1 Pérdida de capacidad por SPI

| SPI | Pérdida base |
|-----|--------------|
| > -0.5 | 0% |
| -1.0 a -0.5 | 5% |
| -1.5 a -1.0 | 15% |
| -2.0 a -1.5 | 30% |
| < -2.0 | 50% |

Multiplicadores: `water_dependency` (high 1.0, medium 0.6, low 0.3), `cooling_type` (once_through 1.2, recirculating 1.0, dry 0.2).

### 7.2 Cálculo de costos

- Costo = capacidad perdida (MW) × horas × precio marginal (USD/MWh)
- Savings = costo_no_action - costo_with_action

---

## 8. Referencias

- EIA Open Data API: https://www.eia.gov/opendata/
- API key: https://www.eia.gov/opendata/register.php
- Docs API: `/docs` (Swagger), `/redoc`

---

## 9. Changelog backend (fix aplicado)

- **GET /economic/prices**: Ahora pasa `region` al cliente EIA. Si `region=TX`, se usan precios de Texas en lugar del promedio nacional.
