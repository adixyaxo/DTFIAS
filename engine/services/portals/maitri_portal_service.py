# engine/services/portals/maitri_portal_service.py
"""
Portal Service for Maitri Antarctic Station.
Conforms strictly to:
- C1: Pure Python (zero HTTP/DB framework imports)
- C3: station_id is set server-side only via STATION_CODE constant
- C4: MUST NOT define issue_command, manage_users, or view_audit
"""
from datetime import datetime, timezone, timedelta
from uuid import UUID
from typing import Any

from engine.interfaces.clock import ClockPort, SystemClock
from engine.interfaces.repositories import (
    StationRepository,
    EnergyRepository,
    AlertRepository,
    CommandRepository,
)
from engine.services.core.energy_service import EnergyService
from engine.services.core.alert_service import AlertService
from engine.services.core.command_service import CommandService
from shared.constants.stations import get_station_metadata


class MaitriPortalService:
    """Server-side portal service for Maitri station operations."""

    # Constraint C3: Station identifier is set server-side only
    STATION_CODE: str = "maitri"

    def __init__(
        self,
        station_repo: StationRepository,
        energy_repo: EnergyRepository,
        alert_repo: AlertRepository,
        command_repo: CommandRepository,
        clock: ClockPort | None = None,
    ) -> None:
        self.station_repo = station_repo
        self.energy_repo = energy_repo
        self.alert_repo = alert_repo
        self.command_repo = command_repo
        self.clock = clock or SystemClock()

        self.energy_service = EnergyService(self.energy_repo, self.clock)
        self.alert_service = AlertService(self.alert_repo, self.clock)
        self.command_service = CommandService(self.command_repo, self.clock)

    async def _resolve_station_id(self) -> UUID | None:
        station = await self.station_repo.get_by_code(self.STATION_CODE)
        return station.id if station else None

    async def get_dashboard_data(self) -> dict[str, Any]:
        """Gathers dashboard telemetry, active alerts, and metadata for Maitri."""
        station_id = await self._resolve_station_id()
        metadata = get_station_metadata(self.STATION_CODE)

        latest_energy = None
        microgrid_status = None
        active_alerts = []
        recent_commands = []

        if station_id:
            latest_energy = await self.energy_service.get_latest_reading(station_id)
            active_alerts = await self.alert_service.list_active(station_id=station_id)
            recent_commands = await self.command_service.get_station_commands(station_id=station_id, limit=5)

            gen = getattr(latest_energy, "generation_kw", None) if latest_energy else None
            con = getattr(latest_energy, "consumption_kw", None) if latest_energy else None
            soc = getattr(latest_energy, "battery_soc_pct", None) if latest_energy else None
            t = getattr(latest_energy, "time", None) if latest_energy else None

            microgrid_status = self.energy_service.evaluate_microgrid_status(
                station_code=self.STATION_CODE,
                generation_kw=gen,
                consumption_kw=con,
                battery_soc_pct=soc,
                reading_time=t,
            )

        return {
            "station_code": self.STATION_CODE,
            "metadata": metadata,
            "latest_energy": latest_energy,
            "microgrid_status": microgrid_status,
            "active_alerts": active_alerts,
            "recent_commands": recent_commands,
        }

    async def get_energy_overview(self) -> dict[str, Any]:
        """Provides detailed energy and power analytics for Maitri."""
        station_id = await self._resolve_station_id()
        latest = None
        history = []
        status = None

        if station_id:
            latest = await self.energy_service.get_latest_reading(station_id)
            now = self.clock.now()
            start_time = now - timedelta(hours=24)
            history = await self.energy_service.get_history(station_id=station_id, start_time=start_time, limit=50)

            gen = getattr(latest, "generation_kw", None) if latest else None
            con = getattr(latest, "consumption_kw", None) if latest else None
            soc = getattr(latest, "battery_soc_pct", None) if latest else None
            t = getattr(latest, "time", None) if latest else None

            status = self.energy_service.evaluate_microgrid_status(
                station_code=self.STATION_CODE,
                generation_kw=gen,
                consumption_kw=con,
                battery_soc_pct=soc,
                reading_time=t,
            )

        return {
            "station_code": self.STATION_CODE,
            "latest": latest,
            "history": history,
            "status": status,
        }

    async def get_latest_reading(self) -> Any | None:
        """Retrieves the latest energy reading for Maitri."""
        station_id = await self._resolve_station_id()
        if not station_id:
            return None
        return await self.energy_service.get_latest_reading(station_id)

    async def get_active_alerts(self) -> list[Any]:
        """Lists active operational alerts for Maitri."""
        station_id = await self._resolve_station_id()
        if not station_id:
            return []
        return await self.alert_service.list_active(station_id=station_id)

    async def acknowledge_alert(self, alert_id: UUID, user_id: UUID) -> Any | None:
        """Acknowledges an alert scoped to Maitri."""
        return await self.alert_service.acknowledge(alert_id=alert_id, user_id=user_id)

    async def get_commands(self, status: str | None = None) -> list[Any]:
        """Views incoming commands issued by HQ for Maitri."""
        station_id = await self._resolve_station_id()
        if not station_id:
            return []
        return await self.command_service.get_station_commands(station_id=station_id, status=status)

    async def execute_command(
        self, command_id: UUID, executed_by: UUID | None, result: str
    ) -> tuple[Any | None, Any]:
        """Station-side execution receipt recording."""
        return await self.command_service.execute_command(
            command_id=command_id,
            executed_by=executed_by,
            result=result,
        )


__all__ = ["MaitriPortalService"]
