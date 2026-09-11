# engine/interfaces/repositories.py
"""
Pure Python Repository Protocols for the DTFIAS Domain Layer.
Conforms to Constraint C1 (zero HTTP/DB/SQLAlchemy dependencies).
Adheres to fixed vocabulary: save, latest, history, get_by_id, get_by_station_id.
"""
from datetime import datetime
from uuid import UUID
from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class StationRepository(Protocol):
    """Protocol for Station data access."""

    async def get_by_id(self, station_id: UUID) -> Any | None:
        ...

    async def get_by_code(self, code: str) -> Any | None:
        ...

    async def list_all(self) -> list[Any]:
        ...


@runtime_checkable
class EnergyRepository(Protocol):
    """Protocol for high-frequency energy readings and microgrid telemetry."""

    async def save(self, reading: Any) -> Any:
        ...

    async def latest(self, station_id: UUID) -> Any | None:
        """Fetch the most recent energy reading for a station."""
        ...

    async def history(
        self, station_id: UUID, start_time: datetime, end_time: datetime | None = None, limit: int = 100
    ) -> list[Any]:
        """Fetch time-series energy readings within a time window."""
        ...


@runtime_checkable
class EnvironmentRepository(Protocol):
    """Protocol for meteorological and environmental sensor readings."""

    async def save(self, reading: Any) -> Any:
        ...

    async def latest(self, station_id: UUID) -> Any | None:
        ...

    async def history(
        self, station_id: UUID, start_time: datetime, end_time: datetime | None = None, limit: int = 100
    ) -> list[Any]:
        ...


@runtime_checkable
class AlertRepository(Protocol):
    """Protocol for Alert Rules and Active Alerts."""

    async def save_rule(self, rule: Any) -> Any:
        ...

    async def list_rules(self, station_id: UUID, active_only: bool = True) -> list[Any]:
        ...

    async def save_active_alert(self, alert: Any) -> Any:
        ...

    async def list_active_alerts(self, station_id: UUID | None = None) -> list[Any]:
        ...

    async def get_active_alert_by_id(self, alert_id: UUID) -> Any | None:
        ...

    async def acknowledge_alert(self, alert_id: UUID, user_id: UUID) -> Any | None:
        ...

    async def resolve_alert(self, alert_id: UUID) -> Any | None:
        ...


@runtime_checkable
class CommandRepository(Protocol):
    """Protocol for Remote Tactical Commands and Executions."""

    async def save(self, command: Any) -> Any:
        ...

    async def get_by_id(self, command_id: UUID) -> Any | None:
        ...

    async def list_by_station(
        self, station_id: UUID, status: str | None = None, limit: int = 50
    ) -> list[Any]:
        ...

    async def update_status(self, command_id: UUID, status: str, rejection_reason: str | None = None) -> Any | None:
        ...

    async def record_execution(self, execution: Any) -> Any:
        ...


@runtime_checkable
class AuditRepository(Protocol):
    """Protocol for Immutable Operational and Security Audit Logs."""

    async def save(self, log_entry: Any) -> Any:
        ...

    async def list_logs(
        self,
        station_id: UUID | None = None,
        user_id: UUID | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[Any]:
        ...


@runtime_checkable
class UserRepository(Protocol):
    """Protocol for Profiles, Roles, and Permissions."""

    async def get_by_id(self, user_id: UUID) -> Any | None:
        ...

    async def get_by_email(self, email: str) -> Any | None:
        ...

    async def get_by_employee_code(self, code: str) -> Any | None:
        ...

    async def save(self, profile: Any) -> Any:
        ...

    async def list_all(self, limit: int = 100) -> list[Any]:
        ...


__all__ = [
    "StationRepository",
    "EnergyRepository",
    "EnvironmentRepository",
    "AlertRepository",
    "CommandRepository",
    "AuditRepository",
    "UserRepository",
]
