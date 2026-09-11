# app/schemas/audit.py
"""
Pydantic V2 schemas for Immutable Audit Logs.
Conforms to docs/database.md audit_logs table (Constraint C7).
"""
from datetime import datetime
from uuid import UUID
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class AuditLogBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    action: str
    entity_type: str
    entity_id: UUID | None = None
    old_value: dict[str, Any] | None = None
    new_value: dict[str, Any] | None = None
    ip_address: str | None = None


class AuditLogCreate(AuditLogBase):
    user_id: UUID | None = None
    station_id: UUID | None = None


class AuditLogResponse(AuditLogBase):
    id: UUID
    user_id: UUID | None = None
    station_id: UUID | None = None
    created_at: datetime


__all__ = ["AuditLogBase", "AuditLogCreate", "AuditLogResponse"]
