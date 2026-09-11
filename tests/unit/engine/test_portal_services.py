# tests/unit/engine/test_portal_services.py
"""
Unit tests for Portal Services (MaitriPortalService, BharatiPortalService, HQPortalService).
Verifies:
- Constraint C3: station_id is set server-side
- Constraint C4: Segregation of duties between station portals and HQ
"""
import pytest
from uuid import uuid4
from datetime import datetime, timezone

from engine.services.portals.maitri_portal_service import MaitriPortalService
from engine.services.portals.bharati_portal_service import BharatiPortalService
from engine.services.portals.hq_portal_service import HQPortalService
from shared.models.enums import CommandType


class MockStation:
    def __init__(self, code, name):
        self.id = uuid4()
        self.code = code
        self.name = name


class MockStationRepo:
    def __init__(self):
        self.stations = [
            MockStation("maitri", "Maitri Research Station"),
            MockStation("bharati", "Bharati Antarctic Station"),
        ]

    async def get_by_code(self, code):
        for s in self.stations:
            if s.code == code.lower():
                return s
        return None

    async def list_all(self):
        return self.stations


class MockEnergyRepo:
    def __init__(self):
        self.readings = []

    async def save(self, r):
        self.readings.append(r)
        return r

    async def latest(self, station_id):
        return None

    async def history(self, station_id, start_time, end_time=None, limit=100):
        return []


class MockAlertRepo:
    async def list_active_alerts(self, station_id=None):
        return []

    async def save_active_alert(self, a):
        return a

    async def acknowledge_alert(self, alert_id, user_id):
        return None


class MockCommandRepo:
    def __init__(self):
        self.commands = []

    async def save(self, c):
        c["id"] = uuid4()
        self.commands.append(c)
        return c

    async def list_by_station(self, station_id, status=None, limit=50):
        return []

    async def execute_command(self, command_id, executed_by, result):
        return None, {"executed": True}


class MockAuditRepo:
    async def list_logs(self, station_id=None, user_id=None, action=None, limit=100):
        return []


class MockUserRepo:
    async def list_all(self, limit=100):
        return []


@pytest.mark.asyncio
async def test_maitri_portal_service_station_scoping():
    station_repo = MockStationRepo()
    service = MaitriPortalService(
        station_repo=station_repo,
        energy_repo=MockEnergyRepo(),
        alert_repo=MockAlertRepo(),
        command_repo=MockCommandRepo(),
    )
    # Constraint C3 verification
    assert service.STATION_CODE == "maitri"

    data = await service.get_dashboard_data()
    assert data["station_code"] == "maitri"
    assert data["metadata"]["name"] == "Maitri"


@pytest.mark.asyncio
async def test_bharati_portal_service_station_scoping():
    station_repo = MockStationRepo()
    service = BharatiPortalService(
        station_repo=station_repo,
        energy_repo=MockEnergyRepo(),
        alert_repo=MockAlertRepo(),
        command_repo=MockCommandRepo(),
    )
    # Constraint C3 verification
    assert service.STATION_CODE == "bharati"

    data = await service.get_dashboard_data()
    assert data["station_code"] == "bharati"
    assert data["metadata"]["name"] == "Bharati"


def test_constraint_c4_segregation_of_duties():
    """Maitri and Bharati portal services MUST NOT define issue_command, manage_users, or view_audit."""
    prohibited = ["issue_command", "manage_users", "view_audit"]
    for method in prohibited:
        assert not hasattr(MaitriPortalService, method), f"C4 breach: MaitriPortalService defines {method}"
        assert not hasattr(BharatiPortalService, method), f"C4 breach: BharatiPortalService defines {method}"
        assert hasattr(HQPortalService, method), f"HQPortalService must define {method}"


@pytest.mark.asyncio
async def test_hq_portal_service_operations():
    station_repo = MockStationRepo()
    cmd_repo = MockCommandRepo()
    service = HQPortalService(
        station_repo=station_repo,
        energy_repo=MockEnergyRepo(),
        alert_repo=MockAlertRepo(),
        command_repo=cmd_repo,
        audit_repo=MockAuditRepo(),
        user_repo=MockUserRepo(),
    )

    # 1. Multi-station overview
    overview = await service.get_overview()
    assert len(overview["stations"]) == 2

    # 2. HQ-exclusive command issuance (C4)
    cmd = await service.issue_command(
        station_id=uuid4(),
        created_by=uuid4(),
        command_type=CommandType.ENERGY_CONTROL,
        parameters={"generator_id": "DG-1", "action": "START"},
    )
    assert cmd["status"] == "PENDING"
    assert len(cmd_repo.commands) == 1
