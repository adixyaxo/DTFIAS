# engine/domain/users/user.py
"""
Pure domain User entities for DTFIAS.
Conforms to Constraint C1 (pure Python, zero HTTP/DB dependencies).
Pydantic V2 syntax only.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from engine.domain.users.role import Role


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    full_name: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: UUID
    roles: list[Role] = Field(default_factory=list)
    created_at: datetime | None = None


# Alias for backward compatibility
User = UserResponse

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserResponse", "User", "Role"]

