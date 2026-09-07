# app/models/station.py
"""
SQLAlchemy ORM models for Stations and Spatial Areas.
Conforms to docs/database.md.
"""
from datetime import datetime, date, timezone
import uuid
from typing import Optional, List
from sqlalchemy import (
    Text, Float, Integer, Date, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import StationStatus, StationType


class Station(Base):
    """Antarctic research station (Maitri, Bharati, etc.). Extensible via rows."""
    __tablename__ = "stations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    station_type: Mapped[StationType] = mapped_column(
        SAEnum(StationType, name="station_type", native_enum=True),
        nullable=False,
    )
    status: Mapped[StationStatus] = mapped_column(
        SAEnum(StationStatus, name="station_status", native_enum=True),
        default=StationStatus.ACTIVE,
        nullable=False,
    )
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    elevation_m: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    commissioned_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    areas: Mapped[List["StationArea"]] = relationship("StationArea", back_populates="station", cascade="all, delete-orphan")
    assets: Mapped[List["Asset"]] = relationship("Asset", back_populates="station")
    user_grants: Mapped[List["StationAccess"]] = relationship("StationAccess", back_populates="station")


class StationArea(Base):
    """Spatial hierarchy within a station (Main Facility, Generator Room, etc.)."""
    __tablename__ = "station_areas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id", ondelete="CASCADE"), nullable=False)
    parent_area_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("station_areas.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    area_type: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    station: Mapped["Station"] = relationship("Station", back_populates="areas")
    children: Mapped[List["StationArea"]] = relationship("StationArea", backref="parent_area", remote_side=[id])
