# app/models/auth.py
"""
SQLAlchemy ORM models for Auth and RBAC domains.
Conforms to docs/database.md and scripts/migrations/001_initial_schema.sql.
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    String, Text, Boolean, DateTime, ForeignKey, Table, Column, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import ProfileStatus, AccessLevel


class Profile(Base):
    """Application user profile — maps 1:1 to auth.users in Supabase."""
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    employee_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    designation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProfileStatus] = mapped_column(
        SAEnum(ProfileStatus, name="profile_status", native_enum=True),
        default=ProfileStatus.ACTIVE,
        nullable=False,
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    roles: Mapped[List["Role"]] = relationship("Role", secondary="user_roles", back_populates="users")
    station_grants: Mapped[List["StationAccess"]] = relationship("StationAccess", back_populates="user")


class Role(Base):
    """Application roles (SUPER_ADMIN, HQ_ADMIN, STATION_OPERATOR, etc.)."""
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    users: Mapped[List["Profile"]] = relationship("Profile", secondary="user_roles", back_populates="roles")
    permissions: Mapped[List["Permission"]] = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    """Fine-grained permission codes (e.g. station.read, command.create)."""
    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    roles: Mapped[List["Role"]] = relationship("Role", secondary="role_permissions", back_populates="permissions")


class UserRole(Base):
    """Many-to-many junction: Profile ↔ Role."""
    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)


class RolePermission(Base):
    """Many-to-many junction: Role ↔ Permission."""
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)


class StationAccess(Base):
    """Station-level access grant, independent of global role."""
    __tablename__ = "station_access"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)
    access_level: Mapped[AccessLevel] = mapped_column(
        SAEnum(AccessLevel, name="access_level", native_enum=True),
        default=AccessLevel.READ,
        nullable=False,
    )
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    granted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)

    user: Mapped["Profile"] = relationship("Profile", foreign_keys=[user_id], back_populates="station_grants")
    station: Mapped["Station"] = relationship("Station", back_populates="user_grants")
