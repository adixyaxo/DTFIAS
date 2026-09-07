# app/models/sensor.py
"""
SQLAlchemy ORM models for Sensors and Sensor Configurations.
Conforms to docs/database.md.
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    Text, Float, Integer, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import SensorStatus


class SensorType(Base):
    """Lookup table for sensor metrics (TEMPERATURE, PRESSURE, BATTERY_SOC, etc.)."""
    __tablename__ = "sensor_types"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    default_unit: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    sensors: Mapped[List["Sensor"]] = relationship("Sensor", back_populates="sensor_type")


class Sensor(Base):
    """Physical or virtual sensor attached to an asset at a station."""
    __tablename__ = "sensors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True)
    sensor_type_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sensor_types.id"), nullable=False)
    sensor_code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    unit: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[SensorStatus] = mapped_column(
        SAEnum(SensorStatus, name="sensor_status", native_enum=True),
        default=SensorStatus.ACTIVE,
        nullable=False,
    )
    last_reading_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    asset: Mapped[Optional["Asset"]] = relationship("Asset", back_populates="sensors")
    sensor_type: Mapped["SensorType"] = relationship("SensorType", back_populates="sensors")
    configurations: Mapped[List["SensorConfiguration"]] = relationship("SensorConfiguration", back_populates="sensor", cascade="all, delete-orphan")


class SensorConfiguration(Base):
    """Operational parameters, thresholds, and calibration offsets for a sensor."""
    __tablename__ = "sensor_configurations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    sampling_interval_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    min_threshold: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_threshold: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calibration_offset: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    effective_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="configurations")
