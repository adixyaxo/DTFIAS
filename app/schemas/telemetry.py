# app/schemas/telemetry.py
"""
Pydantic V2 schemas for High-Frequency Telemetry Domains.
Conforms to docs/database.md energy_readings, environment_readings, asset_readings.
"""
from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from shared.models.enums import ReadingQuality


class EnergyReadingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    generation_kw: float | None = None
    consumption_kw: float | None = None
    battery_soc_pct: float | None = None
    voltage_v: float | None = None
    current_a: float | None = None
    fuel_consumption_lph: float | None = None
    quality: ReadingQuality = ReadingQuality.GOOD


class EnergyReadingCreate(EnergyReadingBase):
    station_id: UUID
    energy_asset_id: UUID | None = None
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnergyReadingResponse(EnergyReadingBase):
    time: datetime
    station_id: UUID
    energy_asset_id: UUID | None = None


class EnvironmentReadingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    temperature_c: float | None = None
    humidity_pct: float | None = None
    pressure_hpa: float | None = None
    wind_speed_mps: float | None = None
    wind_direction_deg: float | None = None
    solar_radiation_wm2: float | None = None
    quality: ReadingQuality = ReadingQuality.GOOD


class EnvironmentReadingCreate(EnvironmentReadingBase):
    station_id: UUID
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EnvironmentReadingResponse(EnvironmentReadingBase):
    time: datetime
    station_id: UUID


class AssetReadingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    metric: str
    value: float
    unit: str | None = None
    quality: ReadingQuality = ReadingQuality.GOOD


class AssetReadingCreate(AssetReadingBase):
    asset_id: UUID
    sensor_id: UUID | None = None
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssetReadingResponse(AssetReadingBase):
    time: datetime
    asset_id: UUID
    sensor_id: UUID | None = None


class TelemetryStreamEvent(BaseModel):
    """Payload serialized for SSE /stream events."""
    station_id: str
    timestamp: str
    generation_kw: float | None = None
    consumption_kw: float | None = None
    battery_soc_pct: float | None = None
    temperature_c: float | None = None
    wind_speed_mps: float | None = None
    staleness_seconds: int = 0


__all__ = [
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
]
