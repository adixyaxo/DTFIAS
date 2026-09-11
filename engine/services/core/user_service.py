# engine/services/core/user_service.py
"""
Domain User Service for managing profiles and roles.
Conforms to Constraint C1 (pure Python, zero HTTP/DB framework imports).
"""
from uuid import UUID
from typing import Any

from engine.interfaces.repositories import UserRepository


class UserService:
    """Core domain logic for users and RBAC."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_user_by_id(self, user_id: UUID) -> Any | None:
        """Retrieves a user by their UUID."""
        return await self.repository.get_by_id(user_id)

    async def get_user_by_employee_code(self, code: str) -> Any | None:
        """Retrieves a user by their employee code."""
        return await self.repository.get_by_employee_code(code)

    async def get_user_by_email(self, email: str) -> Any | None:
        """Retrieves a user by their email/username."""
        return await self.repository.get_by_email(email)

    async def register_user(self, profile_data: dict[str, Any]) -> Any:
        """Registers or creates a new user profile."""
        return await self.repository.save(profile_data)

    async def list_users(self, limit: int = 100) -> list[Any]:
        """Lists users up to a limit."""
        return await self.repository.list_all(limit=limit)


__all__ = ["UserService"]
