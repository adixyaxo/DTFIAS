# engine/services/portals/hq_portal_service.py
"""
Portal Service for NCPOR Mission Control (Headquarters).
Conforms strictly to:
- C1: Pure Python (zero HTTP/DB framework imports)
- C4: EXCLUSIVELY implements issue_command, manage_users, and view_audit
"""
import asyncio
from datetime import datetime, timezone
from uuid import UUID
from typing import Any

from engine.interfaces.clock import ClockPort, SystemClock
from engine.interfaces.repositories import (
    StationRepository,
    EnergyRepository,
    AlertRepository,
    CommandRepository,
    AuditRepository,
    UserRepository,
)
from engine.services.core.energy_service import EnergyService
from engine.services.core.alert_service import AlertService
from engine.services.core.command_service import CommandService
from shared.models.enums import CommandType


class HQPortalService:
    """Server-side portal service for NCPOR HQ Mission Control."""

    def __init__(
        self,
        station_repo: StationRepository,
        energy_repo: EnergyRepository,
        alert_repo: AlertRepository,
        command_repo: CommandRepository,
        audit_repo: AuditRepository,
        user_repo: UserRepository,
        clock: ClockPort | None = None,
    ) -> None:
        self.station_repo = station_repo
        self.energy_repo = energy_repo
        self.alert_repo = alert_repo
        self.command_repo = command_repo
        self.audit_repo = audit_repo
        self.user_repo = user_repo
        self.clock = clock or SystemClock()

        self.energy_service = EnergyService(self.energy_repo, self.clock)
        self.alert_service = AlertService(self.alert_repo, self.clock)
        self.command_service = CommandService(self.command_repo, self.clock)

    async def get_overview(self) -> dict[str, Any]:
        """Provides high-level multi-station monitoring for NCPOR commanders."""
        # Fetch station list and all active alerts sequentially to avoid SQLAlchemy session concurrency issues
        stations = await self.station_repo.list_all()
        all_active_alerts = await self.alert_service.list_active()

        # Partition alerts by station in-memory to eliminate redundant per-station DB queries
        alerts_by_station: dict[UUID, list[Any]] = {}
        for alert in all_active_alerts:
            stn_id = getattr(alert, "station_id", None)
            if stn_id:
                alerts_by_station.setdefault(stn_id, []).append(alert)

        # Fetch all station energy readings sequentially to avoid SQLAlchemy session concurrency issues
        energy_readings = []
        for stn in stations:
            try:
                reading = await self.energy_service.get_latest_reading(stn.id)
                energy_readings.append(reading)
            except Exception as e:
                energy_readings.append(e)

        station_summaries = []
        for stn, latest_energy in zip(stations, energy_readings):
            if isinstance(latest_energy, Exception):
                latest_energy = None
            station_alerts = alerts_by_station.get(stn.id, [])
            status = self.energy_service.evaluate_microgrid_status(
                station_code=stn.code,
                generation_kw=getattr(latest_energy, "generation_kw", None) if latest_energy else None,
                consumption_kw=getattr(latest_energy, "consumption_kw", None) if latest_energy else None,
                battery_soc_pct=getattr(latest_energy, "battery_soc_pct", None) if latest_energy else None,
                reading_time=getattr(latest_energy, "time", None) if latest_energy else None,
            )
            station_summaries.append({
                "station": stn,
                "latest_energy": latest_energy,
                "microgrid_status": status,
                "active_alert_count": len(station_alerts),
            })

        return {
            "stations": station_summaries,
            "total_active_alerts": len(all_active_alerts),
            "alerts": all_active_alerts[:10],
        }


    # Constraint C4: EXCLUSIVELY defined on HQPortalService
    async def issue_command(
        self,
        station_id: UUID,
        created_by: UUID,
        command_type: CommandType,
        parameters: dict[str, Any] | None = None,
        expires_at: datetime | None = None,
    ) -> Any:
        """Issues a remote tactical command to an Antarctic base."""
        return await self.command_service.issue_command(
            station_id=station_id,
            created_by=created_by,
            command_type=command_type,
            parameters=parameters,
            expires_at=expires_at,
        )

    # Constraint C4: EXCLUSIVELY defined on HQPortalService
    async def manage_users(self) -> list[Any]:
        """Lists and manages personnel and application profiles."""
        return await self.user_repo.list_all()

    # Constraint C4: EXCLUSIVELY defined on HQPortalService
    async def view_audit(
        self,
        station_id: UUID | None = None,
        user_id: UUID | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[Any]:
        """Inspects immutable system audit trail."""
        return await self.audit_repo.list_logs(
            station_id=station_id,
            user_id=user_id,
            action=action,
            limit=limit,
        )


__all__ = ["HQPortalService"]
