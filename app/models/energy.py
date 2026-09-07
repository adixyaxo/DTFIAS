# app/models/energy.py
"""
SQLAlchemy ORM models for Energy Systems and Microgrid Topology.
Conforms to docs/database.md.
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    Text, Float, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import EnergySourceType, AssetStatus


class EnergySystem(Base):
    """Overall microgrid energy system per station."""
    __tablename__ = "energy_systems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    sources: Mapped[List["EnergySource"]] = relationship("EnergySource", back_populates="energy_system", cascade="all, delete-orphan")


class EnergySource(Base):
    """Discrete generation or storage component (Solar Array, Diesel GenSet 1, etc.)."""
    __tablename__ = "energy_sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    energy_system_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("energy_systems.id"), nullable=False)
    source_type: Mapped[EnergySourceType] = mapped_column(
        SAEnum(EnergySourceType, name="energy_source_type", native_enum=True),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    capacity_kw: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[AssetStatus] = mapped_column(
        SAEnum(AssetStatus, name="asset_status", native_enum=True),
        default=AssetStatus.OPERATIONAL,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    energy_system: Mapped["EnergySystem"] = relationship("EnergySystem", back_populates="sources")


class EnergyAsset(Base):
    """Junction mapping energy sources to physical equipment assets."""
    __tablename__ = "energy_assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    energy_source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("energy_sources.id"), nullable=False)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False)
