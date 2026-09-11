# engine/services/core/command_service.py
"""
Domain Command Service for Remote Commands, State Transitions, and Executions.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any

from engine.interfaces.clock import ClockPort, SystemClock
from engine.interfaces.repositories import CommandRepository
from shared.models.enums import CommandType, CommandStatus


class CommandService:
    """Core domain logic for tactical command lifecycle management."""

    def __init__(self, repository: CommandRepository, clock: ClockPort | None = None) -> None:
        self.repository = repository
        self.clock = clock or SystemClock()

    async def issue_command(
        self,
        station_id: UUID,
        created_by: UUID,
        command_type: CommandType,
        parameters: dict[str, Any] | None = None,
        expires_at: datetime | None = None,
    ) -> Any:
        """Issues a new remote command in PENDING state."""
        now = self.clock.now()
        payload = {
            "station_id": station_id,
            "created_by": created_by,
            "command_type": command_type,
            "parameters": parameters or {},
            "status": CommandStatus.PENDING,
            "created_at": now,
            "expires_at": expires_at,
            "updated_at": now,
        }
        return await self.repository.save(payload)

    async def validate_command(self, command_id: UUID) -> Any | None:
        """Station-side validation of a received command."""
        command = await self.repository.get_by_id(command_id)
        if not command:
            return None

        # Check if already expired
        if hasattr(command, "expires_at") and command.expires_at:
            if self.clock.now() > command.expires_at:
                return await self.repository.update_status(
                    command_id=command_id,
                    status=CommandStatus.EXPIRED,
                    rejection_reason="Command expired prior to validation",
                )

        return await self.repository.update_status(command_id=command_id, status=CommandStatus.VALIDATED)

    async def reject_command(self, command_id: UUID, reason: str) -> Any | None:
        """Station-side or safety interlock rejection of a command."""
        return await self.repository.update_status(
            command_id=command_id,
            status=CommandStatus.REJECTED,
            rejection_reason=reason,
        )

    async def execute_command(
        self,
        command_id: UUID,
        executed_by: UUID | None,
        result: str,
        result_metadata: dict[str, Any] | None = None,
    ) -> tuple[Any | None, Any]:
        """Executes a command and records execution outcome."""
        now = self.clock.now()
        updated_command = await self.repository.update_status(
            command_id=command_id,
            status=CommandStatus.EXECUTED,
        )
        execution_payload = {
            "command_id": command_id,
            "executed_by": executed_by,
            "result": result,
            "result_metadata": result_metadata or {},
            "executed_at": now,
        }
        execution_receipt = await self.repository.record_execution(execution_payload)
        return updated_command, execution_receipt

    async def fail_command(self, command_id: UUID, reason: str) -> Any | None:
        """Marks a command execution as failed."""
        return await self.repository.update_status(
            command_id=command_id,
            status=CommandStatus.FAILED,
            rejection_reason=reason,
        )

    async def get_station_commands(
        self, station_id: UUID, status: str | None = None, limit: int = 50
    ) -> list[Any]:
        """Lists commands targeted at a specific station."""
        return await self.repository.list_by_station(station_id=station_id, status=status, limit=limit)


__all__ = ["CommandService"]
