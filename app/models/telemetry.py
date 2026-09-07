# app/models/telemetry.py
"""
SQLAlchemy ORM models for High-Frequency Telemetry Domains.
Conforms to docs/database.md (30-day rolling time-series).
"""
from datetime import datetime, timezone
import uuid
from typing import Optional
from sqlalchemy import (
    Text, Float, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base
from shared.models.enums import ReadingQuality


class EnergyReading(Base):
    """High-frequency energy generation, consumption, and storage telemetry."""
    __tablename__ = "energy_readings"

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True, default=lambda: datetime.now(timezone.utc))
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), primary_key=True)
    energy_asset_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
    generation_kw: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    consumption_kw: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    battery_soc_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    voltage_v: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    current_a: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fuel_consumption_lph: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality: Mapped[ReadingQuality] = mapped_column(
        SAEnum(ReadingQuality, name="reading_quality", native_enum=True),
        default=ReadingQuality.GOOD,
        nullable=False,
    )


class EnvironmentReading(Base):
    """High-frequency weather, meteorological, and environmental readings."""
    __tablename__ = "environment_readings"

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True, default=lambda: datetime.now(timezone.utc))
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), primary_key=True)
    temperature_c: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    humidity_pct: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pressure_hpa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_speed_mps: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_direction_deg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    solar_radiation_wm2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    quality: Mapped[ReadingQuality] = mapped_column(
        SAEnum(ReadingQuality, name="reading_quality", native_enum=True),
        default=ReadingQuality.GOOD,
        nullable=False,
    )


class AssetReading(Base):
    """Generic telemetry time-series for specialized asset metrics."""
    __tablename__ = "asset_readings"

    time: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True, default=lambda: datetime.now(timezone.utc))
    asset_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), primary_key=True)
    metric: Mapped[str] = mapped_column(Text, primary_key=True)
    sensor_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("sensors.id"), nullable=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality: Mapped[ReadingQuality] = mapped_column(
        SAEnum(ReadingQuality, name="reading_quality", native_enum=True),
        default=ReadingQuality.GOOD,
        nullable=False,
    )
