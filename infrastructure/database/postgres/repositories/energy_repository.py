# infrastructure/database/postgres/repositories/energy_repository.py
"""
PostgreSQL implementation of EnergyRepository protocol.
"""
from datetime import datetime
from uuid import UUID
from typing import Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.telemetry import EnergyReading
from engine.interfaces.repositories import EnergyRepository


class PostgresEnergyRepository(EnergyRepository):
    """PostgreSQL adapter for Energy telemetry queries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, reading: Any) -> EnergyReading:
        if isinstance(reading, EnergyReading):
            model = reading
        elif isinstance(reading, dict):
            model = EnergyReading(**reading)
        else:
            model = EnergyReading(**reading.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def latest(self, station_id: UUID) -> EnergyReading | None:
        query = (
            select(EnergyReading)
            .where(EnergyReading.station_id == station_id)
            .order_by(desc(EnergyReading.time))
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def history(
        self, station_id: UUID, start_time: datetime, end_time: datetime | None = None, limit: int = 100
    ) -> list[EnergyReading]:
        query = (
            select(EnergyReading)
            .where(EnergyReading.station_id == station_id)
            .where(EnergyReading.time >= start_time)
        )
        if end_time:
            query = query.where(EnergyReading.time <= end_time)

        query = query.order_by(desc(EnergyReading.time)).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())


__all__ = ["PostgresEnergyRepository"]
