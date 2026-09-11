# app/schemas/user.py
"""
Pydantic V2 validation schemas for Users and Profiles.
Conforms to docs/database.md profiles table.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from shared.models.enums import ProfileStatus


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    employee_code: str
    full_name: str
    designation: str | None = None
    organization: str | None = None
    phone: str | None = None
    status: ProfileStatus = ProfileStatus.ACTIVE
    avatar_url: str | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    full_name: str | None = None
    designation: str | None = None
    organization: str | None = None
    phone: str | None = None
    status: ProfileStatus | None = None
    avatar_url: str | None = None


class UserResponse(UserBase):
    id: UUID
    email: EmailStr | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


# Alias for backward compatibility
User = UserResponse

__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserResponse", "User"]


