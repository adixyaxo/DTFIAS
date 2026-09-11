# infrastructure/database/postgres/repositories/command_repository.py
"""
PostgreSQL implementation of CommandRepository protocol.
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.command import Command, CommandExecution
from engine.interfaces.repositories import CommandRepository
from shared.models.enums import CommandStatus


class PostgresCommandRepository(CommandRepository):
    """PostgreSQL adapter for remote command dispatch and lifecycle logging."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, command: Any) -> Command:
        if isinstance(command, Command):
            model = command
        elif isinstance(command, dict):
            model = Command(**command)
        else:
            model = Command(**command.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_by_id(self, command_id: UUID) -> Command | None:
        query = (
            select(Command)
            .where(Command.id == command_id)
            .options(selectinload(Command.executions))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_by_station(
        self, station_id: UUID, status: str | None = None, limit: int = 50
    ) -> list[Command]:
        query = (
            select(Command)
            .where(Command.station_id == station_id)
            .options(selectinload(Command.executions))
            .order_by(desc(Command.created_at))
            .limit(limit)
        )
        if status:
            query = query.where(Command.status == status)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update_status(
        self, command_id: UUID, status: str, rejection_reason: str | None = None
    ) -> Command | None:
        command = await self.get_by_id(command_id)
        if not command:
            return None

        command.status = CommandStatus(status) if isinstance(status, str) else status
        command.updated_at = datetime.now(timezone.utc)
        if rejection_reason:
            command.rejection_reason = rejection_reason

        await self.session.commit()
        await self.session.refresh(command)
        return command

    async def record_execution(self, execution: Any) -> CommandExecution:
        if isinstance(execution, CommandExecution):
            model = execution
        elif isinstance(execution, dict):
            model = CommandExecution(**execution)
        else:
            model = CommandExecution(**execution.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model


__all__ = ["PostgresCommandRepository"]
