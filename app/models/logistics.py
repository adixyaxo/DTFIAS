# app/models/logistics.py
"""
SQLAlchemy ORM models for Inventory, Stock Movements, and Polar Shipments.
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
from shared.models.enums import InventoryUnit, TransactionType, ShipmentStatus


class InventoryItem(Base):
    """Master catalogue of tracked polar consumables and spares."""
    __tablename__ = "inventory_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unit: Mapped[InventoryUnit] = mapped_column(
        SAEnum(InventoryUnit, name="inventory_unit", native_enum=True),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    stocks: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="item")


class Inventory(Base):
    """Current stock balance per item per station."""
    __tablename__ = "inventory"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    minimum_threshold: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    item: Mapped["InventoryItem"] = relationship("InventoryItem", back_populates="stocks")


class InventoryTransaction(Base):
    """Provenance audit for stock adjustments, receipts, and consumptions."""
    __tablename__ = "inventory_transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    transaction_type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType, name="transaction_type", native_enum=True),
        nullable=False,
    )
    quantity_delta: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transacted_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    transacted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    shipment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=True)


class Shipment(Base):
    """Polar resupply convoy or vessel shipment."""
    __tablename__ = "shipments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin: Mapped[str] = mapped_column(Text, nullable=False)
    destination_station_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stations.id"), nullable=False)
    status: Mapped[ShipmentStatus] = mapped_column(
        SAEnum(ShipmentStatus, name="shipment_status", native_enum=True),
        default=ShipmentStatus.PLANNED,
        nullable=False,
    )
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    items: Mapped[List["ShipmentItem"]] = relationship("ShipmentItem", back_populates="shipment", cascade="all, delete-orphan")


class ShipmentItem(Base):
    """Manifest line item within a shipment."""
    __tablename__ = "shipment_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)

    shipment: Mapped["Shipment"] = relationship("Shipment", back_populates="items")
