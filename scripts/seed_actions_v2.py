"""Seed the new 15 heuristic actions into the database.

This script populates the actions table with the new action catalog
corresponding to the 15 heuristics from the technical document.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from src.db.session import get_session
from src.db.models import Action


NEW_ACTIONS_CATALOG = [
    # ============================================================
    # H1: Persistence Trigger - Gatillo de Inicio Confirmado
    # ============================================================
    {
        "code": "H1_MONITORING_INTENSIFICATION",
        "title": "Intensificación de Monitoreo",
        "description": "Incrementar frecuencia de monitoreo SPI de mensual a semanal para detectar deterioro temprano.",
        "heuristic": "H1",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Detección temprana +7 días de anticipación",
        "base_cost": 5000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "monitoring_frequency": {"options": ["daily", "weekly"], "default": "weekly"},
            "alert_sectors": {"options": ["agricultural", "industrial", "municipal", "all"], "default": ["all"]},
        },
    },
    {
        "code": "H1_STAKEHOLDER_ALERT",
        "title": "Alerta a Partes Interesadas",
        "description": "Notificación formal a sectores clave (agrícola, industrial, municipal) sobre inicio de sequía.",
        "heuristic": "H1",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Preparación adelantada +5 días efectivos",
        "base_cost": 2000.0,
        "default_urgency_days": 3,
        "parameter_schema": {
            "sectors": {"options": ["agricultural", "industrial", "municipal", "all"], "default": ["all"]},
        },
    },
    {
        "code": "H1_RESOURCE_PREPOSITION",
        "title": "Preposicionamiento de Recursos",
        "description": "Movilizar y preposicionar recursos de respuesta antes de que sean necesarios.",
        "heuristic": "H1",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Reducción tiempo de respuesta 50%",
        "base_cost": 15000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "resource_level": {"options": ["moderate", "high"], "default": "moderate"},
        },
    },

    # ============================================================
    # H2: Flash Drought - Sequía Relámpago
    # ============================================================
    {
        "code": "H2_FLASH_DROUGHT_ALERT",
        "title": "Alerta de Sequía Relámpago",
        "description": "Emisión de alerta urgente por deterioro acelerado de condiciones hídricas.",
        "heuristic": "H2",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Respuesta acelerada -3 días tiempo de reacción",
        "base_cost": 3000.0,
        "default_urgency_days": 1,
        "parameter_schema": {
            "alert_level": {"options": ["warning", "urgent", "critical"], "default": "urgent"},
        },
    },
    {
        "code": "H2_RAPID_RESPONSE_ACTIVATION",
        "title": "Activación de Respuesta Rápida",
        "description": "Movilizar equipos de respuesta rápida y recursos pre-posicionados.",
        "heuristic": "H2",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Reducción tiempo implementación 50%",
        "base_cost": 25000.0,
        "default_urgency_days": 2,
        "parameter_schema": {
            "response_teams": {"min": 2, "max": 10, "default": 5},
        },
    },
    {
        "code": "H2_EMERGENCY_COMMUNICATION",
        "title": "Comunicación de Emergencia",
        "description": "Campaña de comunicación urgente a sector agrícola sobre condiciones de flash drought.",
        "heuristic": "H2",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Alcance 80% productores en 24h",
        "base_cost": 8000.0,
        "default_urgency_days": 1,
        "parameter_schema": {
            "channels": {"options": ["sms", "radio", "social_media"], "default": ["sms", "radio"]},
        },
    },

    # ============================================================
    # H3: Seasonality Check - Validación Estacional
    # ============================================================
    {
        "code": "H3_VALIDATED_MONITORING",
        "title": "Monitoreo con Validación Estacional",
        "description": "Monitoreo que considera contexto estacional para evitar falsas alarmas.",
        "heuristic": "H3",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Reduce falsas alarmas 80%",
        "base_cost": 3000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },
    {
        "code": "H3_SEASONAL_ADVISORY",
        "title": "Aviso Estacional Contextualizado",
        "description": "Comunicación pública que explica condiciones en contexto estacional.",
        "heuristic": "H3",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Mejora comprensión pública",
        "base_cost": 2000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },

    # ============================================================
    # H4: Phenological Stress - Estrés Fenológico
    # ============================================================
    {
        "code": "H4_AGRICULTURAL_ALERT",
        "title": "Alerta Agrícola por Estrés Fenológico",
        "description": "Alerta a productores sobre riesgo de pérdida de cultivos en etapa crítica.",
        "heuristic": "H4",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Mitigación potencial 20% pérdida",
        "base_cost": 5000.0,
        "default_urgency_days": 3,
        "parameter_schema": {
            "crops": {"options": ["maiz", "frijol", "trigo", "sorgo"], "default": ["maiz"]},
        },
    },
    {
        "code": "H4_IRRIGATION_PRIORITY",
        "title": "Priorización de Riego Agrícola",
        "description": "Reasignar agua disponible a cultivos en etapa fenológica crítica.",
        "heuristic": "H4",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Reducción pérdida cosecha 30%",
        "base_cost": 50000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "allocation_pct": {"min": 10, "max": 50, "default": 25},
        },
    },
    {
        "code": "H4_CROP_INSURANCE_ACTIVATION",
        "title": "Activación de Seguros de Cosecha",
        "description": "Iniciar proceso de activación de seguros agrícolas por sequía.",
        "heuristic": "H4",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Cobertura financiera para productores",
        "base_cost": 1000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },

    # ============================================================
    # H5: Trend Prediction - Predicción de Tendencia
    # ============================================================
    {
        "code": "H5_TREND_ALERT",
        "title": "Alerta de Tendencia Negativa",
        "description": "Comunicar tendencia estadísticamente significativa de degradación.",
        "heuristic": "H5",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Anticipación de 4-8 semanas",
        "base_cost": 2000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },
    {
        "code": "H5_SCENARIO_PROJECTION",
        "title": "Proyección de Escenarios",
        "description": "Generar proyecciones de SPI para los próximos 3-6 meses.",
        "heuristic": "H5",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Mejora planificación de recursos",
        "base_cost": 5000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "projection_months": {"min": 3, "max": 12, "default": 6},
        },
    },
    {
        "code": "H5_PREEMPTIVE_RESTRICTIONS",
        "title": "Restricciones Preventivas por Tendencia",
        "description": "Implementar restricciones leves antes de deterioro proyectado.",
        "heuristic": "H5",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Evitar 15% de impacto futuro",
        "base_cost": 10000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "restriction_level": {"options": ["voluntary", "recommended", "mandatory"], "default": "recommended"},
        },
    },

    # ============================================================
    # H6: Wet Season Failure - Falla de Temporada Húmeda
    # ============================================================
    {
        "code": "H6_SUSTAINED_RESTRICTIONS",
        "title": "Restricciones Sostenidas (Cerrojo Estacional)",
        "description": "Mantener restricciones hasta próxima temporada húmeda exitosa.",
        "heuristic": "H6",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Prevenir agotamiento de reservas",
        "base_cost": 0.0,
        "default_urgency_days": 30,
        "parameter_schema": {
            "review_period_days": {"min": 30, "max": 180, "default": 90},
        },
    },
    {
        "code": "H6_LONG_TERM_PLANNING",
        "title": "Planificación de Largo Plazo",
        "description": "Activar planes de contingencia para déficit estructural.",
        "heuristic": "H6",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Preparación para 12+ meses de déficit",
        "base_cost": 5000.0,
        "default_urgency_days": 30,
        "parameter_schema": {},
    },
    {
        "code": "H6_RESERVE_MANAGEMENT",
        "title": "Gestión de Reservas Estratégicas",
        "description": "Implementar protocolo de gestión de reservas para temporada seca extendida.",
        "heuristic": "H6",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Extender reservas 20%",
        "base_cost": 15000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },

    # ============================================================
    # H7: Reservoir Lag - Inercia Hidrológica
    # ============================================================
    {
        "code": "H7_RESTRICTION_HOLD",
        "title": "Mantener Restricciones (Inercia Hidrológica)",
        "description": "No relajar restricciones hasta validación de almacenamiento físico.",
        "heuristic": "H7",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Evitar recaída prematura",
        "base_cost": 0.0,
        "default_urgency_days": 30,
        "parameter_schema": {
            "reservoir_threshold_pct": {"min": 50, "max": 80, "default": 60},
        },
    },
    {
        "code": "H7_RESERVOIR_VALIDATION",
        "title": "Validación de Niveles de Embalse",
        "description": "Verificar físicamente niveles de embalse antes de relajar medidas.",
        "heuristic": "H7",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Decisiones basadas en datos reales",
        "base_cost": 3000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },
    {
        "code": "H7_PHASED_RELAXATION",
        "title": "Relajación Escalonada",
        "description": "Protocolo de relajación gradual de restricciones.",
        "heuristic": "H7",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Transición controlada",
        "base_cost": 2000.0,
        "default_urgency_days": 30,
        "parameter_schema": {},
    },

    # ============================================================
    # H8: Groundwater Proxy - Acuíferos
    # ============================================================
    {
        "code": "H8_PUMPING_RESTRICTION",
        "title": "Restricción de Bombeo Subterráneo",
        "description": "Limitar extracción de agua subterránea para proteger acuíferos.",
        "heuristic": "H8",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Reducir extracción 20%",
        "base_cost": 15000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "reduction_pct": {"min": 10, "max": 40, "default": 20},
        },
    },
    {
        "code": "H8_AQUIFER_MONITORING",
        "title": "Monitoreo Intensivo de Acuíferos",
        "description": "Incrementar frecuencia de medición de niveles freáticos.",
        "heuristic": "H8",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Detección temprana de agotamiento",
        "base_cost": 8000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "monitoring_frequency": {"options": ["weekly", "biweekly", "monthly"], "default": "biweekly"},
        },
    },
    {
        "code": "H8_ALTERNATIVE_SOURCES",
        "title": "Activación de Fuentes Alternativas",
        "description": "Buscar y activar fuentes alternativas de agua.",
        "heuristic": "H8",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Diversificación de suministro",
        "base_cost": 50000.0,
        "default_urgency_days": 30,
        "parameter_schema": {},
    },

    # ============================================================
    # H9: Scale Differential - Sequía Verde
    # ============================================================
    {
        "code": "H9_FALSE_RECOVERY_ALERT",
        "title": "Alerta de Falsa Recuperación",
        "description": "Comunicar que lluvia reciente no significa fin de sequía.",
        "heuristic": "H9",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Evitar relajación prematura pública",
        "base_cost": 5000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "channels": {"options": ["media", "social_media", "official"], "default": ["official", "media"]},
        },
    },
    {
        "code": "H9_SUSTAINED_MONITORING",
        "title": "Monitoreo Sostenido",
        "description": "Mantener vigilancia intensiva a pesar de mejoras aparentes.",
        "heuristic": "H9",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Prevenir sorpresas",
        "base_cost": 3000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },
    {
        "code": "H9_PUBLIC_COMMUNICATION",
        "title": "Comunicación Pública sobre Sequía Verde",
        "description": "Campaña explicando que paisaje verde no significa fin de crisis hídrica.",
        "heuristic": "H9",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Mantener comportamiento de conservación",
        "base_cost": 10000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },

    # ============================================================
    # H10: Drought Magnitude - Magnitud Acumulada
    # ============================================================
    {
        "code": "H10_MAGNITUDE_BASED_RESPONSE",
        "title": "Respuesta Basada en Magnitud Histórica",
        "description": "Escalar intensidad de respuesta según percentil histórico.",
        "heuristic": "H10",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Respuesta proporcional a severidad",
        "base_cost": 20000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "response_tier": {"options": ["tier_1", "tier_2", "tier_3"], "default": "tier_2"},
        },
    },
    {
        "code": "H10_HISTORICAL_COMPARISON",
        "title": "Comparación Histórica",
        "description": "Generar informe comparando evento actual con sequías históricas.",
        "heuristic": "H10",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Contexto para decisiones",
        "base_cost": 3000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },
    {
        "code": "H10_ESCALATED_MEASURES",
        "title": "Medidas Escaladas",
        "description": "Activar medidas de nivel superior según magnitud acumulada.",
        "heuristic": "H10",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Respuesta proporcional",
        "base_cost": 30000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },

    # ============================================================
    # H11: Markov Transition - Predicción Probabilística
    # ============================================================
    {
        "code": "H11_PREEMPTIVE_ACTIVATION",
        "title": "Activación Preventiva por Probabilidad",
        "description": "Activar medidas antes de transición probable a estado severo.",
        "heuristic": "H11",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Adelantar respuesta 2-4 semanas",
        "base_cost": 15000.0,
        "default_urgency_days": 14,
        "parameter_schema": {
            "probability_threshold": {"min": 0.5, "max": 0.9, "default": 0.6},
        },
    },
    {
        "code": "H11_PROBABILITY_ALERT",
        "title": "Alerta Basada en Probabilidad",
        "description": "Comunicar probabilidad de deterioro a tomadores de decisión.",
        "heuristic": "H11",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Decisiones informadas",
        "base_cost": 2000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },
    {
        "code": "H11_CONTINGENCY_PREPARATION",
        "title": "Preparación de Contingencia",
        "description": "Preparar planes de contingencia basados en escenarios probabilísticos.",
        "heuristic": "H11",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Preparación anticipada",
        "base_cost": 8000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },

    # ============================================================
    # H12: Weather Whiplash - Volatilidad Climática
    # ============================================================
    {
        "code": "H12_MAXIMUM_CONSERVATION",
        "title": "Conservación Máxima (Post-Volatilidad)",
        "description": "Medidas de conservación intensivas tras transición rápida húmedo-seco.",
        "heuristic": "H12",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Reducir consumo 15%",
        "base_cost": 25000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "conservation_target_pct": {"min": 10, "max": 25, "default": 15},
        },
    },
    {
        "code": "H12_INFRASTRUCTURE_PROTECTION",
        "title": "Protección de Infraestructura",
        "description": "Evaluar y proteger infraestructura estresada por cambios rápidos.",
        "heuristic": "H12",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Prevenir fallas de infraestructura",
        "base_cost": 20000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },
    {
        "code": "H12_VOLATILITY_MANAGEMENT",
        "title": "Gestión de Volatilidad en Embalses",
        "description": "Ajustar reglas de operación de embalses para clima volátil.",
        "heuristic": "H12",
        "spi_min": -999.0,
        "spi_max": 999.0,
        "impact_formula": "Retención conservadora de agua",
        "base_cost": 10000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },

    # ============================================================
    # H13: Cooling Towers - Eficiencia Industrial
    # ============================================================
    {
        "code": "H13_COC_MANDATE",
        "title": "Mandato de Ciclos de Concentración",
        "description": "Requerir CoC >= 5 en torres de enfriamiento industriales.",
        "heuristic": "H13",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Reducción consumo industrial 25%",
        "base_cost": 10000.0,
        "default_urgency_days": 30,
        "parameter_schema": {
            "minimum_coc": {"min": 4, "max": 8, "default": 5},
        },
    },
    {
        "code": "H13_INDUSTRIAL_AUDIT",
        "title": "Auditoría Industrial de Agua",
        "description": "Auditoría obligatoria de eficiencia hídrica para grandes consumidores.",
        "heuristic": "H13",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Identificar ahorros potenciales",
        "base_cost": 15000.0,
        "default_urgency_days": 30,
        "parameter_schema": {},
    },
    {
        "code": "H13_WATER_TREATMENT_UPGRADE",
        "title": "Apoyo para Tratamiento de Agua",
        "description": "Asistencia técnica y financiera para mejorar tratamiento de agua de proceso.",
        "heuristic": "H13",
        "spi_min": -999.0,
        "spi_max": -1.5,
        "impact_formula": "Habilitación de mayor CoC",
        "base_cost": 50000.0,
        "default_urgency_days": 60,
        "parameter_schema": {},
    },

    # ============================================================
    # H14: Infrastructure Defense - Gestión de Presión
    # ============================================================
    {
        "code": "H14_NIGHT_PRESSURE_REDUCTION",
        "title": "Reducción de Presión Nocturna",
        "description": "Reducir presión en red 23:00-06:00 para minimizar pérdidas.",
        "heuristic": "H14",
        "spi_min": -999.0,
        "spi_max": -2.0,
        "impact_formula": "Reducir pérdidas 15%",
        "base_cost": 20000.0,
        "default_urgency_days": 7,
        "parameter_schema": {
            "pressure_reduction_pct": {"min": 10, "max": 30, "default": 20},
        },
    },
    {
        "code": "H14_DEMAND_MANAGEMENT",
        "title": "Gestión de Demanda con Tarifas",
        "description": "Implementar tarifas escalonadas punitivas para alto consumo.",
        "heuristic": "H14",
        "spi_min": -999.0,
        "spi_max": -2.0,
        "impact_formula": "Reducir demanda pico 20%",
        "base_cost": 5000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },
    {
        "code": "H14_INFRASTRUCTURE_PROTECTION",
        "title": "Protección de Infraestructura Crítica",
        "description": "Medidas para proteger infraestructura bajo estrés prolongado.",
        "heuristic": "H14",
        "spi_min": -999.0,
        "spi_max": -2.0,
        "impact_formula": "Prevenir fallas sistémicas",
        "base_cost": 30000.0,
        "default_urgency_days": 14,
        "parameter_schema": {},
    },

    # ============================================================
    # H15: Step-Down Recovery - Terminación Escalonada
    # ============================================================
    {
        "code": "H15_PHASED_RELAXATION",
        "title": "Relajación Escalonada de Restricciones",
        "description": "Eliminar restricciones gradualmente: 1)recreativo, 2)riego, 3)industrial.",
        "heuristic": "H15",
        "spi_min": 0.0,
        "spi_max": 999.0,
        "impact_formula": "Normalización controlada",
        "base_cost": 5000.0,
        "default_urgency_days": 30,
        "parameter_schema": {
            "phase_duration_days": {"min": 14, "max": 60, "default": 30},
        },
    },
    {
        "code": "H15_RECOVERY_MONITORING",
        "title": "Monitoreo de Recuperación",
        "description": "Vigilancia intensiva durante fase de recuperación.",
        "heuristic": "H15",
        "spi_min": 0.0,
        "spi_max": 999.0,
        "impact_formula": "Detección de recaída",
        "base_cost": 3000.0,
        "default_urgency_days": 30,
        "parameter_schema": {},
    },
    {
        "code": "H15_PUBLIC_ANNOUNCEMENT",
        "title": "Anuncio Público de Recuperación",
        "description": "Comunicación oficial del inicio de fase de recuperación.",
        "heuristic": "H15",
        "spi_min": 0.0,
        "spi_max": 999.0,
        "impact_formula": "Información al público",
        "base_cost": 2000.0,
        "default_urgency_days": 7,
        "parameter_schema": {},
    },
]


def seed_actions(session: Session):
    """Seed all new actions into the database."""
    print(f"Seeding {len(NEW_ACTIONS_CATALOG)} actions...")

    for action_data in NEW_ACTIONS_CATALOG:
        # Check if action already exists
        existing = session.query(Action).filter(
            Action.code == action_data["code"]
        ).first()

        if existing:
            print(f"  Updating: {action_data['code']}")
            for key, value in action_data.items():
                setattr(existing, key, value)
        else:
            print(f"  Creating: {action_data['code']}")
            action = Action(**action_data)
            session.add(action)

    session.commit()
    print("Done!")


if __name__ == "__main__":
    with get_session() as session:
        seed_actions(session)
