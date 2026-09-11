# infrastructure/database/postgres/repositories/alert_repository.py
"""
PostgreSQL implementation of AlertRepository protocol.
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import AlertRule, ActiveAlert
from engine.interfaces.repositories import AlertRepository
from shared.models.enums import AlertStatus


class PostgresAlertRepository(AlertRepository):
    """PostgreSQL adapter for Alert Rule and Active Alert persistence."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_rule(self, rule: Any) -> AlertRule:
        if isinstance(rule, AlertRule):
            model = rule
        elif isinstance(rule, dict):
            model = AlertRule(**rule)
        else:
            model = AlertRule(**rule.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_rules(self, station_id: UUID, active_only: bool = True) -> list[AlertRule]:
        query = select(AlertRule).where(AlertRule.station_id == station_id)
        if active_only:
            query = query.where(AlertRule.is_active == True)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def save_active_alert(self, alert: Any) -> ActiveAlert:
        if isinstance(alert, ActiveAlert):
            model = alert
        elif isinstance(alert, dict):
            model = ActiveAlert(**alert)
        else:
            model = ActiveAlert(**alert.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_active_alerts(self, station_id: UUID | None = None) -> list[ActiveAlert]:
        query = (
            select(ActiveAlert)
            .where(ActiveAlert.status.in_([AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]))
            .order_by(desc(ActiveAlert.created_at))
        )
        if station_id:
            query = query.where(ActiveAlert.station_id == station_id)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_active_alert_by_id(self, alert_id: UUID) -> ActiveAlert | None:
        query = select(ActiveAlert).where(ActiveAlert.id == alert_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def acknowledge_alert(self, alert_id: UUID, user_id: UUID) -> ActiveAlert | None:
        alert = await self.get_active_alert_by_id(alert_id)
        if not alert:
            return None
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_at = datetime.now(timezone.utc)
        alert.acknowledged_by = user_id
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def resolve_alert(self, alert_id: UUID) -> ActiveAlert | None:
        alert = await self.get_active_alert_by_id(alert_id)
        if not alert:
            return None
        alert.status = AlertStatus.RESOLVED
        await self.session.commit()
        await self.session.refresh(alert)
        return alert


__all__ = ["PostgresAlertRepository"]
