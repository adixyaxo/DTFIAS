# app/models/observation.py
"""
SQLAlchemy ORM model for Scientific Environmental Observations.
Conforms to docs/database.md (permanent scientific data, distinct from telemetry).
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, Dict, Any
from sqlalchemy import (
    Text, Float, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base
from shared.models.enums import ObservationType, ReadingQuality


class ScientificObservation(Base):
    """Permanent scientific observation recorded at Antarctic stations."""
    __tablename__ = "scientific_observations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    observation_type: Mapped[ObservationType] = mapped_column(
        SAEnum(ObservationType, name="observation_type", native_enum=True),
        nullable=False,
    )
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    text_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality: Mapped[ReadingQuality] = mapped_column(
        SAEnum(ReadingQuality, name="reading_quality", native_enum=True),
        default=ReadingQuality.GOOD,
        nullable=False,
    )
    source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSONB, nullable=True)
    recorded_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
