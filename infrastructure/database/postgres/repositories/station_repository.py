# infrastructure/database/postgres/repositories/station_repository.py
"""
PostgreSQL implementation of StationRepository protocol.
"""
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.station import Station, StationArea
from engine.interfaces.repositories import StationRepository


class PostgresStationRepository(StationRepository):
    """PostgreSQL adapter for Station domain queries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, station_id: UUID) -> Station | None:
        query = (
            select(Station)
            .where(Station.id == station_id)
            .options(selectinload(Station.areas))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Station | None:
        query = (
            select(Station)
            .where(Station.code == code.lower())
            .options(selectinload(Station.areas))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Station]:
        query = select(Station).order_by(Station.name.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())


__all__ = ["PostgresStationRepository"]
