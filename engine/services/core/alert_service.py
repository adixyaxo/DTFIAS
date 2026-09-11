# engine/services/core/alert_service.py
"""
Domain Alert Service for evaluating operational thresholds and managing active alerts.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any

from engine.interfaces.clock import ClockPort, SystemClock
from engine.interfaces.repositories import AlertRepository
from shared.models.enums import AlertSeverity, AlertStatus
from shared.constants.thresholds import (
    BATTERY_SOC_CRITICAL_PCT,
    BATTERY_SOC_MIN_PCT,
    GENERATOR_TEMP_MAX_C,
    INDOOR_TEMP_CRITICAL_C,
    INDOOR_TEMP_MIN_WARNING_C,
    WIND_SPEED_BLIZZARD_MPS,
)


class AlertService:
    """Core domain logic for operational polar alerts."""

    def __init__(self, repository: AlertRepository, clock: ClockPort | None = None) -> None:
        self.repository = repository
        self.clock = clock or SystemClock()

    async def raise_alert(
        self,
        station_id: UUID,
        severity: AlertSeverity,
        alert_type: str,
        message: str,
        asset_id: UUID | None = None,
        sensor_id: UUID | None = None,
        alert_rule_id: UUID | None = None,
        expires_at: datetime | None = None,
    ) -> Any:
        """Creates an active alert."""
        payload = {
            "station_id": station_id,
            "asset_id": asset_id,
            "sensor_id": sensor_id,
            "alert_rule_id": alert_rule_id,
            "severity": severity,
            "alert_type": alert_type,
            "message": message,
            "status": AlertStatus.ACTIVE,
            "created_at": self.clock.now(),
            "expires_at": expires_at,
        }
        return await self.repository.save_active_alert(payload)

    async def acknowledge(self, alert_id: UUID, user_id: UUID) -> Any | None:
        """Acknowledges an active alert."""
        return await self.repository.acknowledge_alert(alert_id=alert_id, user_id=user_id)

    async def resolve(self, alert_id: UUID) -> Any | None:
        """Resolves an alert."""
        return await self.repository.resolve_alert(alert_id=alert_id)

    async def list_active(self, station_id: UUID | None = None) -> list[Any]:
        """Lists active alerts, optionally filtered by station."""
        return await self.repository.list_active_alerts(station_id=station_id)

    async def evaluate_telemetry_thresholds(
        self,
        station_id: UUID,
        battery_soc_pct: float | None = None,
        generator_temp_c: float | None = None,
        indoor_temp_c: float | None = None,
        wind_speed_mps: float | None = None,
    ) -> list[Any]:
        """
        Evaluates real-world polar thresholds and automatically raises
        alerts for life-safety critical conditions.
        """
        generated_alerts = []

        # 1. Critical Battery Depletion
        if battery_soc_pct is not None:
            if battery_soc_pct <= BATTERY_SOC_CRITICAL_PCT:
                alert = await self.raise_alert(
                    station_id=station_id,
                    severity=AlertSeverity.CRITICAL,
                    alert_type="POWER_BATTERY_CRITICAL",
                    message=f"Critical battery depletion: {battery_soc_pct:.1f}% (Limit: {BATTERY_SOC_CRITICAL_PCT}%)",
                )
                generated_alerts.append(alert)
            elif battery_soc_pct <= BATTERY_SOC_MIN_PCT:
                alert = await self.raise_alert(
                    station_id=station_id,
                    severity=AlertSeverity.HIGH,
                    alert_type="POWER_BATTERY_LOW",
                    message=f"Low battery state of charge: {battery_soc_pct:.1f}% (Warning: {BATTERY_SOC_MIN_PCT}%)",
                )
                generated_alerts.append(alert)

        # 2. Generator Overheating
        if generator_temp_c is not None and generator_temp_c >= GENERATOR_TEMP_MAX_C:
            alert = await self.raise_alert(
                station_id=station_id,
                severity=AlertSeverity.CRITICAL,
                alert_type="GENERATOR_OVERHEAT",
                message=f"Diesel generator overheating: {generator_temp_c:.1f}°C (Limit: {GENERATOR_TEMP_MAX_C}°C)",
            )
            generated_alerts.append(alert)

        # 3. Life-Safety Habitat Thermal Loss
        if indoor_temp_c is not None:
            if indoor_temp_c <= INDOOR_TEMP_CRITICAL_C:
                alert = await self.raise_alert(
                    station_id=station_id,
                    severity=AlertSeverity.CRITICAL,
                    alert_type="LIFE_SAFETY_FREEZE_RISK",
                    message=f"Habitat freeze hazard: Indoor temp dropped to {indoor_temp_c:.1f}°C!",
                )
                generated_alerts.append(alert)
            elif indoor_temp_c <= INDOOR_TEMP_MIN_WARNING_C:
                alert = await self.raise_alert(
                    station_id=station_id,
                    severity=AlertSeverity.HIGH,
                    alert_type="THERMAL_LOSS_WARNING",
                    message=f"Habitat temperature declining: {indoor_temp_c:.1f}°C",
                )
                generated_alerts.append(alert)

        # 4. Severe Antarctic Blizzard Wind
        if wind_speed_mps is not None and wind_speed_mps >= WIND_SPEED_BLIZZARD_MPS:
            alert = await self.raise_alert(
                station_id=station_id,
                severity=AlertSeverity.HIGH,
                alert_type="METEOROLOGICAL_BLIZZARD",
                message=f"Blizzard gale warning: Wind speed {wind_speed_mps:.1f} m/s (~{wind_speed_mps * 3.6:.0f} km/h)",
            )
            generated_alerts.append(alert)

        return generated_alerts


__all__ = ["AlertService"]
