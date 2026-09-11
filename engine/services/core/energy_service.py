# engine/services/core/energy_service.py
"""
Domain Energy Service for microgrid telemetry, power balancing, and storage analysis.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any

from engine.interfaces.clock import ClockPort, SystemClock
from engine.interfaces.repositories import EnergyRepository
from shared.constants.thresholds import (
    BHARATI_MAX_GENERATION_KW,
    BHARATI_NORMAL_LOAD_KW,
    MAITRI_MAX_GENERATION_KW,
    MAITRI_NORMAL_LOAD_KW,
    BATTERY_SOC_CRITICAL_PCT,
    BATTERY_SOC_MIN_PCT,
    STALENESS_WARNING_SECONDS,
    STALENESS_CRITICAL_SECONDS,
)
from shared.models.enums import ReadingQuality


class EnergyService:
    """Core domain logic for Antarctic station microgrids."""

    def __init__(self, repository: EnergyRepository, clock: ClockPort | None = None) -> None:
        self.repository = repository
        self.clock = clock or SystemClock()

    async def record_reading(
        self,
        station_id: UUID,
        generation_kw: float | None = None,
        consumption_kw: float | None = None,
        battery_soc_pct: float | None = None,
        voltage_v: float | None = None,
        current_a: float | None = None,
        fuel_consumption_lph: float | None = None,
        energy_asset_id: UUID | None = None,
        quality: ReadingQuality = ReadingQuality.GOOD,
        recorded_at: datetime | None = None,
    ) -> Any:
        """Validates and persists an energy telemetry reading."""
        time = recorded_at or self.clock.now()

        # Sanity checking
        if battery_soc_pct is not None:
            battery_soc_pct = max(0.0, min(100.0, float(battery_soc_pct)))

        reading_payload = {
            "time": time,
            "station_id": station_id,
            "energy_asset_id": energy_asset_id,
            "generation_kw": float(generation_kw) if generation_kw is not None else None,
            "consumption_kw": float(consumption_kw) if consumption_kw is not None else None,
            "battery_soc_pct": battery_soc_pct,
            "voltage_v": float(voltage_v) if voltage_v is not None else None,
            "current_a": float(current_a) if current_a is not None else None,
            "fuel_consumption_lph": float(fuel_consumption_lph) if fuel_consumption_lph is not None else None,
            "quality": quality,
        }
        return await self.repository.save(reading_payload)

    async def get_latest_reading(self, station_id: UUID) -> Any | None:
        """Retrieves latest reading for a station."""
        return await self.repository.latest(station_id)

    async def get_history(
        self, station_id: UUID, start_time: datetime, end_time: datetime | None = None, limit: int = 100
    ) -> list[Any]:
        """Retrieves time-series energy readings."""
        return await self.repository.history(
            station_id=station_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
        )

    def evaluate_microgrid_status(
        self,
        station_code: str,
        generation_kw: float | None,
        consumption_kw: float | None,
        battery_soc_pct: float | None,
        reading_time: datetime | None,
    ) -> dict[str, Any]:
        """
        Pure business calculation evaluating microgrid margins, battery warning state,
        and telemetry staleness.
        """
        now = self.clock.now()
        max_gen = BHARATI_MAX_GENERATION_KW if station_code.lower() == "bharati" else MAITRI_MAX_GENERATION_KW
        normal_load = BHARATI_NORMAL_LOAD_KW if station_code.lower() == "bharati" else MAITRI_NORMAL_LOAD_KW

        net_kw = (generation_kw or 0.0) - (consumption_kw or 0.0)
        reserve_margin_pct = 0.0
        if generation_kw and generation_kw > 0:
            reserve_margin_pct = max(0.0, ((max_gen - generation_kw) / max_gen) * 100.0)

        battery_status = "NORMAL"
        if battery_soc_pct is not None:
            if battery_soc_pct <= BATTERY_SOC_CRITICAL_PCT:
                battery_status = "CRITICAL"
            elif battery_soc_pct <= BATTERY_SOC_MIN_PCT:
                battery_status = "WARNING"

        staleness_seconds = 0
        is_stale = False
        if reading_time:
            delta = (now - reading_time).total_seconds()
            staleness_seconds = max(0, int(delta))
            if staleness_seconds >= STALENESS_WARNING_SECONDS:
                is_stale = True

        return {
            "station_code": station_code,
            "max_generation_kw": max_gen,
            "normal_load_kw": normal_load,
            "net_kw": round(net_kw, 2),
            "reserve_margin_pct": round(reserve_margin_pct, 1),
            "battery_status": battery_status,
            "is_stale": is_stale,
            "staleness_seconds": staleness_seconds,
        }

    def evaluate_generator_health(
        self,
        asset_code: str,
        rpm: float,
        oil_pressure_kpa: float,
        exhaust_temp_c: float,
        operating_hours: float
    ) -> dict[str, Any]:
        """
        Predictive maintenance for CHP Generators (e.g. MAN 100kVA).
        Tracks critical telemetry (rpm, oil pressure, exhaust temp) against normal bands.
        Alerts on upcoming major maintenance milestones (10k / 20k / 40k hours).
        """
        status = "NORMAL"
        priority = "NONE"
        alerts = []

        # RPM bounds (1500 RPM for 50Hz generators is standard)
        if rpm < 1450 or rpm > 1550:
            status = "WARNING"
            priority = "HIGH"
            alerts.append(f"Generator RPM out of bounds ({rpm}). Possible governor failure or severe load imbalance.")

        # Oil Pressure bounds (normal typically 300-500 kPa)
        if oil_pressure_kpa < 200:
            status = "CRITICAL"
            priority = "HIGH"
            alerts.append(f"CRITICAL: Low oil pressure ({oil_pressure_kpa} kPa). Risk of imminent engine seizure.")
            
        # Exhaust Temp bounds (normal typically 400-550 C at load)
        if exhaust_temp_c > 600:
            status = "WARNING"
            priority = "MEDIUM"
            alerts.append(f"High exhaust temperature ({exhaust_temp_c}°C). Possible overloading or coolant failure.")

        # Maintenance Milestones
        milestones = [10000, 20000, 40000]
        for milestone in milestones:
            # Alert if within 200 hours of a major milestone
            if 0 <= (milestone - operating_hours) <= 200:
                if status == "NORMAL":
                    status = "MAINTENANCE_DUE"
                priority = "MEDIUM"
                alerts.append(f"Upcoming major maintenance milestone: {milestone} hours. Currently at {round(operating_hours, 1)} hours.")

        return {
            "asset_code": asset_code,
            "status": status,
            "priority": priority,
            "alerts": alerts,
            "operating_hours": round(operating_hours, 1)
        }


__all__ = ["EnergyService"]
