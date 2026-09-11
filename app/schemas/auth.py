# app/schemas/auth.py
"""
Pydantic V2 schemas for Authentication and RBAC tokens/credentials.
"""
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from shared.models.enums import ProfileStatus, AccessLevel


class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 86400
    user_id: UUID
    username: str
    roles: list[str] = Field(default_factory=list)


class TokenPayload(BaseModel):
    sub: str  # User / Profile UUID
    email: EmailStr | None = None
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    station_access: dict[str, str] = Field(default_factory=dict)  # station_id -> access_level
    exp: int


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID
    name: str
    description: str | None = None
    permissions: list[str] = Field(default_factory=list)


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID
    code: str
    description: str | None = None


class StationAccessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    station_id: UUID
    access_level: AccessLevel


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID
    employee_code: str
    full_name: str
    email: EmailStr | None = None
    designation: str | None = None
    organization: str | None = None
    phone: str | None = None
    status: ProfileStatus
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    station_access: list[StationAccessResponse] = Field(default_factory=list)


__all__ = [
    "LoginRequest",
    "TokenResponse",
    "TokenPayload",
    "RoleResponse",
    "PermissionResponse",
    "StationAccessResponse",
    "UserProfileResponse",
]
