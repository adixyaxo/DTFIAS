# app/models/maintenance.py
"""
SQLAlchemy ORM models for Asset Maintenance and Work Orders.
Conforms to docs/database.md.
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    Text, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import MaintenanceType, MaintenanceStatus, MaintenancePriority


class MaintenanceRecord(Base):
    """Scheduled or corrective maintenance activity on an asset."""
    __tablename__ = "maintenance_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    maintenance_type: Mapped[MaintenanceType] = mapped_column(
        SAEnum(MaintenanceType, name="maintenance_type", native_enum=True),
        nullable=False,
    )
    priority: Mapped[MaintenancePriority] = mapped_column(
        SAEnum(MaintenancePriority, name="maintenance_priority", native_enum=True),
        default=MaintenancePriority.MEDIUM,
        nullable=False,
    )
    status: Mapped[MaintenanceStatus] = mapped_column(
        SAEnum(MaintenanceStatus, name="maintenance_status", native_enum=True),
        default=MaintenanceStatus.SCHEDULED,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    performed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    events: Mapped[List["MaintenanceEvent"]] = relationship("MaintenanceEvent", back_populates="record", cascade="all, delete-orphan")


class MaintenanceEvent(Base):
    """Discrete milestones or progress notes within a maintenance activity."""
    __tablename__ = "maintenance_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    maintenance_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("maintenance_records.id", ondelete="CASCADE"), nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recorded_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    record: Mapped["MaintenanceRecord"] = relationship("MaintenanceRecord", back_populates="events")
