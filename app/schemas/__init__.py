# app/schemas/__init__.py
"""
Central exports for all Pydantic V2 validation schemas.
"""
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse, User
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    TokenPayload,
    RoleResponse,
    PermissionResponse,
    StationAccessResponse,
    UserProfileResponse,
)
from app.schemas.station import (
    StationBase,
    StationCreate,
    StationUpdate,
    StationResponse,
    StationAreaBase,
    StationAreaCreate,
    StationAreaResponse,
)
from app.schemas.telemetry import (
    EnergyReadingBase,
    EnergyReadingCreate,
    EnergyReadingResponse,
    EnvironmentReadingBase,
    EnvironmentReadingCreate,
    EnvironmentReadingResponse,
    AssetReadingBase,
    AssetReadingCreate,
    AssetReadingResponse,
    TelemetryStreamEvent,
)
from app.schemas.command import (
    CommandCreate,
    CommandResponse,
    CommandExecutionCreate,
    CommandExecutionResponse,
)
from app.schemas.alert import (
    AlertRuleBase,
    AlertRuleCreate,
    AlertRuleUpdate,
    AlertRuleResponse,
    ActiveAlertBase,
    ActiveAlertCreate,
    ActiveAlertResponse,
    AlertAcknowledgeRequest,
)
from app.schemas.audit import (
    AuditLogBase,
    AuditLogCreate,
    AuditLogResponse,
)

__all__ = [
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "User",
    # Auth
    "LoginRequest",
    "TokenResponse",
    "TokenPayload",
    "RoleResponse",
    "PermissionResponse",
    "StationAccessResponse",
    "UserProfileResponse",
    # Station
    "StationBase",
    "StationCreate",
    "StationUpdate",
    "StationResponse",
    "StationAreaBase",
    "StationAreaCreate",
    "StationAreaResponse",
    # Telemetry
    "EnergyReadingBase",
    "EnergyReadingCreate",
    "EnergyReadingResponse",
    "EnvironmentReadingBase",
    "EnvironmentReadingCreate",
    "EnvironmentReadingResponse",
    "AssetReadingBase",
    "AssetReadingCreate",
    "AssetReadingResponse",
    "TelemetryStreamEvent",
    # Command
    "CommandCreate",
    "CommandResponse",
    "CommandExecutionCreate",
    "CommandExecutionResponse",
    # Alert
    "AlertRuleBase",
    "AlertRuleCreate",
    "AlertRuleUpdate",
    "AlertRuleResponse",
    "ActiveAlertBase",
    "ActiveAlertCreate",
    "ActiveAlertResponse",
    "AlertAcknowledgeRequest",
    # Audit
    "AuditLogBase",
    "AuditLogCreate",
    "AuditLogResponse",
]
