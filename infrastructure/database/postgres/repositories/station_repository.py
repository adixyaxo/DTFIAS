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


# In-memory station caches to avoid redundant remote queries
_STATION_CACHE_BY_CODE: dict[str, Station] = {}
_STATION_ID_CACHE_BY_CODE: dict[str, UUID] = {}


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
        c = code.lower()
        if c in _STATION_CACHE_BY_CODE:
            return _STATION_CACHE_BY_CODE[c]

        query = select(Station).where(Station.code == c)
        result = await self.session.execute(query)
        station = result.scalar_one_or_none()
        if station:
            _STATION_CACHE_BY_CODE[c] = station
            _STATION_ID_CACHE_BY_CODE[c] = station.id
        return station

    async def get_id_by_code(self, code: str) -> UUID | None:
        c = code.lower()
        if c in _STATION_ID_CACHE_BY_CODE:
            return _STATION_ID_CACHE_BY_CODE[c]
        station = await self.get_by_code(code)
        return station.id if station else None

    async def list_all(self) -> list[Station]:
        query = select(Station).order_by(Station.name.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())


__all__ = ["PostgresStationRepository"]
