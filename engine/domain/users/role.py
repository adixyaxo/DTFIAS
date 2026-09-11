# engine/domain/users/role.py
"""
Pure domain Role entity for the domain engine.
Zero HTTP/DB dependencies per Constraint C1.
"""
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class Role(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID | None = None
    name: str
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)


__all__ = ["Role"]
