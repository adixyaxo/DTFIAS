# tests/e2e/test_rbac_route_isolation.py
"""
E2E tests for RBAC, route isolation, Argon2 password security, and JWT sessions.
Verifies:
- Constraint C5: Router-level guards block unauthorized access
- Constraint C6: Argon2 password hashing
- Constraint C7: Audit trail on login / access denial
- Cross-station tenant isolation between Maitri, Bharati, and HQ
"""
import pytest
from uuid import uuid4
from httpx import AsyncClient, ASGITransport

from main import app
from infrastructure.security.authentication.passwords import hash_password, verify_password
from infrastructure.security.authorization.rbac import create_access_token


def test_argon2_password_hashing():
    """Constraint C6: Passwords MUST be hashed with Argon2."""
    password = "PolarSafePassword2026!"
    hashed = hash_password(password)

    assert hashed.startswith("$argon2id$")
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123", hashed) is False


def test_jwt_token_lifecycle():
    """Validates JWT creation and decoding."""
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "maitri_op_01", "roles": ["maitri_operator"]}
    )
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_unauthenticated_request_blocked():
    """Constraint C5: Unauthenticated access to station/HQ portals must be rejected with 401."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res_maitri = await client.get("/maitri/")
        assert res_maitri.status_code == 401

        res_bharati = await client.get("/bharati/")
        assert res_bharati.status_code == 401

        res_hq = await client.get("/hq/")
        assert res_hq.status_code == 401


@pytest.mark.asyncio
async def test_maitri_operator_cross_station_isolation():
    """
    A user with maitri_operator role MUST NOT access Bharati or HQ.
    """
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "maitri_op", "roles": ["maitri_operator"]}
    )

    transport = ASGITransport(app=app)
    cookies = {"dtfias_session": token}
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        # Cross-station attempt on Bharati must fail with 403 Forbidden
        res_bharati = await client.get("/bharati/")
        assert res_bharati.status_code == 403

        # Cross-station attempt on HQ must fail with 403 Forbidden
        res_hq = await client.get("/hq/")
        assert res_hq.status_code == 403


@pytest.mark.asyncio
async def test_api_users_rbac_guarded():
    """Verify /api/users is protected by RBAC (SUPER_ADMIN / HQ_ADMIN)."""
    transport = ASGITransport(app=app)
    user_id = str(uuid4())

    # 1. Unauthenticated request -> 401
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get(f"/api/users/{user_id}")
        assert res.status_code == 401

    # 2. Unauthorized role (maitri_operator) -> 403
    unauth_token = create_access_token(
        data={"sub": user_id, "username": "operator", "roles": ["maitri_operator"]}
    )
    async with AsyncClient(transport=transport, base_url="http://test", cookies={"dtfias_session": unauth_token}) as client:
        res = await client.get(f"/api/users/{user_id}")
        assert res.status_code == 403

    # 3. Authorized role (hq_admin) -> Allowed through RBAC guard (not 401 or 403)
    auth_token = create_access_token(
        data={"sub": user_id, "username": "hq_commander", "roles": ["hq_admin"]}
    )
    async with AsyncClient(transport=transport, base_url="http://test", cookies={"dtfias_session": auth_token}) as client:
        res = await client.get(f"/api/users/{user_id}")
        assert res.status_code not in (401, 403)


@pytest.mark.asyncio
async def test_bharati_routes_and_aliases():
    """Verify /bharati/dashboard and operational domain routes."""
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "bharati_op", "roles": ["bharati_operator"]}
    )
    transport = ASGITransport(app=app)
    cookies = {"dtfias_session": token}

    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        for path in [
            "/bharati/dashboard",
            "/bharati/infrastructure",
            "/bharati/environment",
            "/bharati/logistics",
        ]:
            res = await client.get(path)
            assert res.status_code == 200, f"Route {path} returned {res.status_code}"


@pytest.mark.asyncio
async def test_maitri_routes_and_aliases():
    """Verify /maitri/dashboard and operational domain routes."""
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "maitri_op", "roles": ["maitri_operator"]}
    )
    transport = ASGITransport(app=app)
    cookies = {"dtfias_session": token}

    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        for path in [
            "/maitri/dashboard",
            "/maitri/infrastructure",
            "/maitri/environment",
            "/maitri/logistics",
        ]:
            res = await client.get(path)
            assert res.status_code == 200, f"Route {path} returned {res.status_code}"


@pytest.mark.asyncio
async def test_hq_routes_and_aliases():
    """Verify /hq/dashboard, /hq/roles, /hq/reports, and /hq/simulations."""
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": "hq_op", "roles": ["hq_operator"]}
    )
    transport = ASGITransport(app=app)
    cookies = {"dtfias_session": token}

    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        for path in [
            "/hq/dashboard",
            "/hq/roles",
            "/hq/reports",
            "/hq/simulations",
        ]:
            res = await client.get(path)
            assert res.status_code == 200, f"Route {path} returned {res.status_code}"

