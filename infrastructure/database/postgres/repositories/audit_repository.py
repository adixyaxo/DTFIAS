# infrastructure/database/postgres/repositories/audit_repository.py
"""
PostgreSQL implementation of AuditRepository protocol.
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from engine.interfaces.repositories import AuditRepository


class PostgresAuditRepository(AuditRepository):
    """PostgreSQL adapter for Immutable Audit Logging."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, log_entry: Any) -> AuditLog:
        if isinstance(log_entry, AuditLog):
            model = log_entry
        elif isinstance(log_entry, dict):
            model = AuditLog(**log_entry)
        else:
            model = AuditLog(**log_entry.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_logs(
        self,
        station_id: UUID | None = None,
        user_id: UUID | None = None,
        action: str | None = None,
        limit: int = 100,
    ) -> list[AuditLog]:
        query = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
        if station_id:
            query = query.where(AuditLog.station_id == station_id)
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
        if action:
            query = query.where(AuditLog.action == action)

        result = await self.session.execute(query)
        return list(result.scalars().all())


__all__ = ["PostgresAuditRepository"]
