# app/models/personnel.py
"""
SQLAlchemy ORM models for Personnel and Expeditions.
Conforms to docs/database.md.
"""
from datetime import datetime, date, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    Text, Date, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import ProfileStatus, AssignmentStatus, HealthStatus


class Personnel(Base):
    """Application-level expedition personnel record."""
    __tablename__ = "personnel"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True)
    employee_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    designation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[ProfileStatus] = mapped_column(
        SAEnum(ProfileStatus, name="profile_status", native_enum=True),
        default=ProfileStatus.ACTIVE,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    assignments: Mapped[List["StationAssignment"]] = relationship("StationAssignment", back_populates="personnel")
    health_records: Mapped[List["PersonnelHealthStatus"]] = relationship("PersonnelHealthStatus", back_populates="personnel")


class StationAssignment(Base):
    """Deployment of an expeditioner to a station."""
    __tablename__ = "station_assignments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    personnel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)
    station_role: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    arrival_date: Mapped[date] = mapped_column(Date, nullable=False)
    departure_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[AssignmentStatus] = mapped_column(
        SAEnum(AssignmentStatus, name="assignment_status", native_enum=True),
        default=AssignmentStatus.ACTIVE,
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    personnel: Mapped["Personnel"] = relationship("Personnel", back_populates="assignments")


class PersonnelHealthStatus(Base):
    """Basic fitness and operational health status."""
    __tablename__ = "personnel_health_status"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    personnel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("personnel.id", ondelete="CASCADE"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    status: Mapped[HealthStatus] = mapped_column(
        SAEnum(HealthStatus, name="health_status", native_enum=True),
        nullable=False,
    )
    condition: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    recorded_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)

    personnel: Mapped["Personnel"] = relationship("Personnel", back_populates="health_records")
