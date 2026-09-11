# tests/unit/engine/test_core_services.py
"""
Unit tests for Core Domain Services (EnergyService, AlertService, CommandService).
Tests domain logic without requiring a live database.
"""
import pytest
from datetime import datetime, timezone
from uuid import uuid4

from engine.interfaces.clock import SystemClock
from engine.services.core.energy_service import EnergyService
from engine.services.core.alert_service import AlertService
from engine.services.core.command_service import CommandService
from shared.models.enums import AlertSeverity, CommandType, CommandStatus


class InMemoryEnergyRepo:
    def __init__(self):
        self.readings = []

    async def save(self, reading):
        self.readings.append(reading)
        return reading

    async def latest(self, station_id):
        matching = [r for r in self.readings if r["station_id"] == station_id]
        return matching[-1] if matching else None

    async def history(self, station_id, start_time, end_time=None, limit=100):
        return [r for r in self.readings if r["station_id"] == station_id][:limit]


class InMemoryAlertRepo:
    def __init__(self):
        self.rules = []
        self.alerts = []

    async def save_rule(self, rule):
        self.rules.append(rule)
        return rule

    async def list_rules(self, station_id, active_only=True):
        return self.rules

    async def save_active_alert(self, alert):
        alert["id"] = uuid4()
        self.alerts.append(alert)
        return alert

    async def list_active_alerts(self, station_id=None):
        return self.alerts

    async def get_active_alert_by_id(self, alert_id):
        for a in self.alerts:
            if a["id"] == alert_id:
                return a
        return None

    async def acknowledge_alert(self, alert_id, user_id):
        a = await self.get_active_alert_by_id(alert_id)
        if a:
            a["status"] = "ACKNOWLEDGED"
        return a

    async def resolve_alert(self, alert_id):
        a = await self.get_active_alert_by_id(alert_id)
        if a:
            a["status"] = "RESOLVED"
        return a


class InMemoryCommandRepo:
    def __init__(self):
        self.commands = []
        self.executions = []

    async def save(self, command):
        command["id"] = uuid4()
        self.commands.append(command)
        return command

    async def get_by_id(self, command_id):
        for c in self.commands:
            if c["id"] == command_id:
                return c
        return None

    async def list_by_station(self, station_id, status=None, limit=50):
        return [c for c in self.commands if c["station_id"] == station_id][:limit]

    async def update_status(self, command_id, status, rejection_reason=None):
        c = await self.get_by_id(command_id)
        if c:
            c["status"] = status
            if rejection_reason:
                c["rejection_reason"] = rejection_reason
        return c

    async def record_execution(self, execution):
        execution["id"] = uuid4()
        self.executions.append(execution)
        return execution


@pytest.mark.asyncio
async def test_energy_service_record_and_microgrid_status():
    repo = InMemoryEnergyRepo()
    service = EnergyService(repo)
    station_id = uuid4()

    # 1. Record reading
    reading = await service.record_reading(
        station_id=station_id,
        generation_kw=280.0,
        consumption_kw=220.0,
        battery_soc_pct=85.0,
    )
    assert reading["generation_kw"] == 280.0
    assert len(repo.readings) == 1

    # 2. Evaluate status
    status = service.evaluate_microgrid_status(
        station_code="bharati",
        generation_kw=280.0,
        consumption_kw=220.0,
        battery_soc_pct=85.0,
        reading_time=datetime.now(timezone.utc),
    )
    assert status["net_kw"] == 60.0
    assert status["battery_status"] == "NORMAL"
    assert status["is_stale"] is False


@pytest.mark.asyncio
async def test_alert_service_threshold_triggers():
    repo = InMemoryAlertRepo()
    service = AlertService(repo)
    station_id = uuid4()

    # Depleted battery should generate CRITICAL alert
    alerts = await service.evaluate_telemetry_thresholds(
        station_id=station_id,
        battery_soc_pct=10.0,  # Below critical (15%)
        generator_temp_c=100.0,  # Overheating (Limit 95°C)
    )
    assert len(alerts) == 2
    assert any(a["severity"] == AlertSeverity.CRITICAL for a in alerts)


@pytest.mark.asyncio
async def test_command_service_state_machine():
    repo = InMemoryCommandRepo()
    service = CommandService(repo)
    station_id = uuid4()
    operator_id = uuid4()

    # Issue command
    cmd = await service.issue_command(
        station_id=station_id,
        created_by=operator_id,
        command_type=CommandType.ENERGY_CONTROL,
        parameters={"action": "switch_to_diesel_generator_2"},
    )
    assert cmd["status"] == CommandStatus.PENDING

    # Validate
    validated = await service.validate_command(cmd["id"])
    assert validated["status"] == CommandStatus.VALIDATED

    # Execute
    executed_cmd, receipt = await service.execute_command(
        command_id=cmd["id"],
        executed_by=operator_id,
        result="SUCCESS: Generator 2 online and synchronised.",
    )
    assert executed_cmd["status"] == CommandStatus.EXECUTED
    assert receipt["result"].startswith("SUCCESS")
