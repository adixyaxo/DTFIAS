# app/models/__init__.py
"""
Central export for all SQLAlchemy ORM models across DTFIAS.
"""
from app.models.auth import (
    Profile,
    Role,
    Permission,
    UserRole,
    RolePermission,
    StationAccess,
)
from app.models.station import Station, StationArea
from app.models.asset import AssetType, Asset, AssetStatusHistory
from app.models.sensor import SensorType, Sensor, SensorConfiguration
from app.models.telemetry import EnergyReading, EnvironmentReading, AssetReading
from app.models.energy import EnergySystem, EnergySource, EnergyAsset
from app.models.personnel import Personnel, StationAssignment, PersonnelHealthStatus
from app.models.command import Command, CommandExecution
from app.models.alert import AlertRule, ActiveAlert
from app.models.audit import AuditLog
from app.models.logistics import (
    InventoryItem,
    Inventory,
    InventoryTransaction,
    Shipment,
    ShipmentItem,
)
from app.models.maintenance import MaintenanceRecord, MaintenanceEvent
from app.models.observation import ScientificObservation

# Aliases for backward compatibility
User = Profile

__all__ = [
    "Profile",
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "StationAccess",
    "Station",
    "StationArea",
    "AssetType",
    "Asset",
    "AssetStatusHistory",
    "SensorType",
    "Sensor",
    "SensorConfiguration",
    "EnergyReading",
    "EnvironmentReading",
    "AssetReading",
    "EnergySystem",
    "EnergySource",
    "EnergyAsset",
    "Personnel",
    "StationAssignment",
    "PersonnelHealthStatus",
    "Command",
    "CommandExecution",
    "AlertRule",
    "ActiveAlert",
    "AuditLog",
    "InventoryItem",
    "Inventory",
    "InventoryTransaction",
    "Shipment",
    "ShipmentItem",
    "MaintenanceRecord",
    "MaintenanceEvent",
    "ScientificObservation",
]
