# infrastructure/database/postgres/repositories/user_repository.py
"""
PostgreSQL implementation of UserRepository protocol.
"""
from uuid import UUID
from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.auth import Profile, Role
from engine.interfaces.repositories import UserRepository


class PostgresUserRepository(UserRepository):
    """PostgreSQL adapter for Profile and RBAC queries."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: UUID) -> Profile | None:
        query = (
            select(Profile)
            .where(Profile.id == user_id)
            .options(selectinload(Profile.roles), selectinload(Profile.station_grants))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_employee_code(self, code: str) -> Profile | None:
        query = (
            select(Profile)
            .where(Profile.employee_code == code)
            .options(selectinload(Profile.roles), selectinload(Profile.station_grants))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Profile | None:
        # In Supabase Auth, profiles.id matches auth.users.id.
        # Fallback lookup on employee_code if needed or direct match.
        return await self.get_by_employee_code(email)

    async def save(self, profile: Any) -> Profile:
        if isinstance(profile, Profile):
            model = profile
        elif isinstance(profile, dict):
            model = Profile(**profile)
        else:
            model = Profile(**profile.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_all(self, limit: int = 100) -> list[Profile]:
        query = (
            select(Profile)
            .options(selectinload(Profile.roles))
            .order_by(Profile.full_name.asc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())


__all__ = ["PostgresUserRepository"]
