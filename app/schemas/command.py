# app/schemas/command.py
"""
Pydantic V2 schemas for Remote Commands and Executions.
Conforms to docs/database.md commands & command_executions tables.
"""
from datetime import datetime
from uuid import UUID
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from shared.models.enums import CommandType, CommandStatus


class CommandCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    station_id: UUID
    command_type: CommandType
    parameters: dict[str, Any] = Field(default_factory=dict)
    expires_at: datetime | None = None


class CommandExecutionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    command_id: UUID
    result: str | None = None
    result_metadata: dict[str, Any] = Field(default_factory=dict)


class CommandExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID
    command_id: UUID
    executed_by: UUID | None = None
    result: str | None = None
    result_metadata: dict[str, Any] | None = None
    executed_at: datetime


class CommandResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    id: UUID
    station_id: UUID
    created_by: UUID
    command_type: CommandType
    parameters: dict[str, Any] | None = None
    status: CommandStatus
    rejection_reason: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    updated_at: datetime
    executions: list[CommandExecutionResponse] = Field(default_factory=list)


__all__ = [
    "CommandCreate",
    "CommandResponse",
    "CommandExecutionCreate",
    "CommandExecutionResponse",
]
