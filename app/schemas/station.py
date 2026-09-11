# app/schemas/station.py
"""
Pydantic V2 schemas for Antarctic Stations and Spatial Areas.
Conforms to docs/database.md stations & station_areas tables.
"""
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from shared.models.enums import StationStatus, StationType


class StationAreaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    name: str
    area_type: str | None = None
    description: str | None = None


class StationAreaCreate(StationAreaBase):
    station_id: UUID
    parent_area_id: UUID | None = None


class StationAreaResponse(StationAreaBase):
    id: UUID
    station_id: UUID
    parent_area_id: UUID | None = None
    created_at: datetime | None = None


class StationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    code: str
    name: str
    description: str | None = None
    station_type: StationType = StationType.RESEARCH_STATION
    status: StationStatus = StationStatus.ACTIVE
    latitude: float | None = None
    longitude: float | None = None
    elevation_m: float | None = None
    capacity: int | None = None
    commissioned_at: date | None = None


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    name: str | None = None
    description: str | None = None
    status: StationStatus | None = None
    latitude: float | None = None
    longitude: float | None = None
    elevation_m: float | None = None
    capacity: int | None = None


class StationResponse(StationBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
    areas: list[StationAreaResponse] = Field(default_factory=list)


__all__ = [
    "StationBase",
    "StationCreate",
    "StationUpdate",
    "StationResponse",
    "StationAreaBase",
    "StationAreaCreate",
    "StationAreaResponse",
]
