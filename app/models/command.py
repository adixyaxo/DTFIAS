# app/models/command.py
"""
SQLAlchemy ORM models for Remote Commands and Executions.
Conforms to docs/database.md (HQ requests; station validates/executes).
"""
from datetime import datetime, timezone
import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Text, DateTime, ForeignKey, Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from shared.models.enums import CommandType, CommandStatus


class Command(Base):
    """Remote tactical command issued by HQ to an Antarctic station."""
    __tablename__ = "commands"
    __table_args__ = (
        Index("ix_commands_station_status_created", "station_id", "status", "created_at"),
        Index("ix_commands_created_by", "created_by"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    command_type: Mapped[CommandType] = mapped_column(
        SAEnum(CommandType, name="command_type", native_enum=True),
        nullable=False,
    )
    parameters: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    status: Mapped[CommandStatus] = mapped_column(
        SAEnum(CommandStatus, name="command_status", native_enum=True),
        default=CommandStatus.PENDING,
        nullable=False,
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    executions: Mapped[List["CommandExecution"]] = relationship(
        "CommandExecution", back_populates="command", cascade="all, delete-orphan", lazy="selectin"
    )


class CommandExecution(Base):
    """Execution receipt/outcome recorded by the station operator or automation."""
    __tablename__ = "command_executions"
    __table_args__ = (
        Index("ix_command_executions_command_id", "command_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    command_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("commands.id", ondelete="CASCADE"), nullable=False)
    executed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    command: Mapped["Command"] = relationship("Command", back_populates="executions")
