# app/models/asset.py
"""
SQLAlchemy ORM models for Physical Assets and Equipment.
Conforms to docs/database.md.
"""
from datetime import datetime, date, timezone
import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Text, Date, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import AssetStatus, AssetCriticality


class AssetType(Base):
    """Lookup table for asset categories (Generator, Solar Panel, Fuel Tank, etc.)."""
    __tablename__ = "asset_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="asset_type")


class Asset(Base):
    """Physical asset / piece of equipment deployed at an Antarctic station."""
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    area_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("station_areas.id"), nullable=True)
    asset_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False)
    parent_asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    asset_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    serial_number: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[AssetStatus] = mapped_column(
        SAEnum(AssetStatus, name="asset_status", native_enum=True),
        default=AssetStatus.OPERATIONAL,
        nullable=False,
    )
    criticality: Mapped[AssetCriticality] = mapped_column(
        SAEnum(AssetCriticality, name="asset_criticality", native_enum=True),
        default=AssetCriticality.MEDIUM,
        nullable=False,
    )
    installation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    commissioned_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    station: Mapped["Station"] = relationship("Station", back_populates="assets")
    asset_type: Mapped["AssetType"] = relationship("AssetType", back_populates="assets")
    sensors: Mapped[List["Sensor"]] = relationship("Sensor", back_populates="asset")
    status_history: Mapped[List["AssetStatusHistory"]] = relationship("AssetStatusHistory", back_populates="asset", cascade="all, delete-orphan")


class AssetStatusHistory(Base):
    """Immutable audit log of asset status transitions."""
    __tablename__ = "asset_status_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    old_status: Mapped[Optional[AssetStatus]] = mapped_column(
        SAEnum(AssetStatus, name="asset_status", native_enum=True),
        nullable=True,
    )
    new_status: Mapped[AssetStatus] = mapped_column(
        SAEnum(AssetStatus, name="asset_status", native_enum=True),
        nullable=False,
    )
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    asset: Mapped["Asset"] = relationship("Asset", back_populates="status_history")
