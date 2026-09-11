# app/schemas/alert.py
"""
Pydantic V2 schemas for Alert Rules and Active Alerts.
Conforms to docs/database.md alert_rules & active_alerts tables.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from shared.models.enums import AlertSeverity, AlertStatus


class AlertRuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    name: str
    description: str | None = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    condition_expression: str
    is_active: bool = True


class AlertRuleCreate(AlertRuleBase):
    station_id: UUID


class AlertRuleUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    name: str | None = None
    description: str | None = None
    severity: AlertSeverity | None = None
    condition_expression: str | None = None
    is_active: bool | None = None


class AlertRuleResponse(AlertRuleBase):
    id: UUID
    station_id: UUID
    created_by: UUID | None = None
    created_at: datetime


class ActiveAlertBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    station_id: UUID
    severity: AlertSeverity
    alert_type: str
    message: str
    status: AlertStatus = AlertStatus.ACTIVE


class ActiveAlertCreate(ActiveAlertBase):
    asset_id: UUID | None = None
    sensor_id: UUID | None = None
    alert_rule_id: UUID | None = None
    expires_at: datetime | None = None


class AlertAcknowledgeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    alert_id: UUID
    note: str | None = None


class ActiveAlertResponse(ActiveAlertBase):
    id: UUID
    asset_id: UUID | None = None
    sensor_id: UUID | None = None
    alert_rule_id: UUID | None = None
    created_at: datetime
    acknowledged_at: datetime | None = None
    acknowledged_by: UUID | None = None
    expires_at: datetime | None = None


__all__ = [
    "AlertRuleBase",
    "AlertRuleCreate",
    "AlertRuleUpdate",
    "AlertRuleResponse",
    "ActiveAlertBase",
    "ActiveAlertCreate",
    "ActiveAlertResponse",
    "AlertAcknowledgeRequest",
]
