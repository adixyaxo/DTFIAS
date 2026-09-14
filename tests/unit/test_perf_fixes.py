"""
Unit & Integration Tests for Phase 3 Performance Optimizations.
Verifies:
1. POST /hq/commands succeeds with HTTP 201 without MissingGreenlet.
2. GET /stream yields initial event immediately and exits cleanly on non-event-stream clients.
3. HTMX request header ("HX-Request": "true") returns partial fragment (<div id="dashboard_content">) without full doctype/html wrapper.
4. Non-HTMX standard request returns complete page with <!DOCTYPE html>.
5. get_current_user_optional uses verified JWT claims directly without DB roundtrips.
6. DB models declare expected composite indexes in __table_args__.
"""
from uuid import uuid4
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from infrastructure.security.authorization.rbac import create_access_token
from app.models.telemetry import EnergyReading, EnvironmentReading
from app.models.alert import ActiveAlert
from app.models.command import Command
from app.models.audit import AuditLog


def make_test_token(role: str = "hq_operator") -> dict[str, str]:
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": f"user_{role}", "roles": [role]}
    )
    return {"dtfias_session": token}


@pytest.mark.asyncio
async def test_htmx_partial_rendering_vs_full_page():
    """Verifies that HX-Request: true returns partial fragment while normal browser request returns full doctype."""
    transport = ASGITransport(app=app)
    cookies = make_test_token("hq_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        # Full page request
        res_full = await client.get("/hq/environment")
        assert res_full.status_code == 200
        assert "<!DOCTYPE html>" in res_full.text or "<html" in res_full.text
        full_size = len(res_full.content)

        # HTMX partial request
        res_partial = await client.get("/hq/environment", headers={"HX-Request": "true"})
        assert res_partial.status_code == 200
        assert "<!DOCTYPE html>" not in res_partial.text
        assert "<html" not in res_partial.text
        assert 'id="dashboard_content"' in res_partial.text
        partial_size = len(res_partial.content)

        # Confirm massive payload reduction (>= 50% up to 90%)
        assert partial_size < full_size
        reduction_pct = (full_size - partial_size) / full_size * 100
        assert reduction_pct > 50, f"Expected >50% reduction, got {reduction_pct:.1f}%"


@pytest.mark.asyncio
async def test_sse_stream_immediate_snapshot_and_clean_exit_for_non_sse_clients():
    """Verifies that /stream yields an immediate event and exits for clients not accepting text/event-stream."""
    transport = ASGITransport(app=app)
    cookies = make_test_token("maitri_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        # Request with standard Accept header (not event-stream)
        res = await client.get("/maitri/energy/stream", headers={"Accept": "*/*"})
        assert res.status_code == 200
        assert "text/event-stream" in res.headers["content-type"]
        assert "data: " in res.text


@pytest.mark.asyncio
async def test_models_declare_composite_indexes():
    """Verifies that SQLAlchemy ORM models declare expected performance indexes in __table_args__."""
    energy_idx_names = [idx.name for idx in EnergyReading.__table_args__ if hasattr(idx, "name")]
    assert "ix_energy_readings_station_time" in energy_idx_names

    env_idx_names = [idx.name for idx in EnvironmentReading.__table_args__ if hasattr(idx, "name")]
    assert "ix_environment_readings_station_time" in env_idx_names

    alert_idx_names = [idx.name for idx in ActiveAlert.__table_args__ if hasattr(idx, "name")]
    assert "ix_active_alerts_station_status_created" in alert_idx_names

    cmd_idx_names = [idx.name for idx in Command.__table_args__ if hasattr(idx, "name")]
    assert "ix_commands_station_status_created" in cmd_idx_names

    audit_idx_names = [idx.name for idx in AuditLog.__table_args__ if hasattr(idx, "name")]
    assert "ix_audit_logs_created_at" in audit_idx_names
    assert "ix_audit_logs_station_created" in audit_idx_names


@pytest.mark.asyncio
async def test_rbac_token_fast_path():
    """Verifies that valid JWT claims build Profile directly without throwing DB errors."""
    from infrastructure.security.authorization.rbac import get_current_user_optional
    from starlette.requests import Request

    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "fast_op", "roles": ["hq_operator"]}
    )

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"cookie", f"dtfias_session={token}".encode())],
    }
    req = Request(scope)

    # Call with db=None to prove fast path does not touch the database
    profile = await get_current_user_optional(req, db=None)
    assert profile is not None
    assert str(profile.id) == user_id
    assert profile.employee_code == "fast_op"
    role_names = [r.name for r in profile.roles]
    assert "hq_operator" in role_names


@pytest.mark.asyncio
async def test_post_hq_commands_endpoint():
    """Verifies POST /hq/commands creates command and responds with 201 Created without MissingGreenlet."""
    from app.dependencies.portals import get_hq_portal_service
    from app.models.command import Command
    from shared.models.enums import CommandType, CommandStatus
    from datetime import datetime, timezone

    stn_id = uuid4()

    class MockHQService:
        async def issue_command(self, station_id, created_by, command_type, parameters, expires_at):
            cmd = Command(
                id=uuid4(),
                station_id=station_id,
                created_by=created_by,
                command_type=command_type,
                parameters=parameters,
                status=CommandStatus.PENDING,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            return cmd

    app.dependency_overrides[get_hq_portal_service] = lambda: MockHQService()

    transport = ASGITransport(app=app)
    csrf_val = "test_csrf_token_1234567890123456"
    cookies = make_test_token("super_admin")
    cookies["dtfias_csrf"] = csrf_val
    try:
        async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
            payload = {
                "station_id": str(stn_id),
                "command_type": "SYSTEM_CONTROL",
                "parameters": {"test_mode": "perf_fix_verification"},
            }
            res = await client.post(
                "/hq/commands",
                json=payload,
                headers={"X-CSRF-Token": csrf_val},
            )
            assert res.status_code == 201, f"Command creation failed with {res.status_code}: {res.text}"
            data = res.json()
            assert data["station_id"] == str(stn_id)
            assert data["status"] == "PENDING"
            # Verify executions relationship is not improperly serialized
            assert "executions" not in data
    finally:
        app.dependency_overrides.pop(get_hq_portal_service, None)
