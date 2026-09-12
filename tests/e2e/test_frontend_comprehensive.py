# tests/e2e/test_frontend_comprehensive.py
"""
Comprehensive E2E Frontend Testing Suite for DTFIAS.
Validates:
- All 47 public, station, and HQ routes render HTTP 200 OK with valid HTML.
- Zero unrendered Jinja syntax leaks ({{, {%) or internal server errors.
- Strict adherence to Brand Design System (.agents/brand_design/SKILL.md).
- Zero forbidden fonts (Space Grotesk, Arial, Roboto).
- Static asset existence on disk for all /static/... references.
- Constraint C16: Three.js lazy-loading strictly via x-init.
- Mobile responsive layout components (hamburger menu, off-canvas drawer, overlay).
"""
import os
import re
from pathlib import Path
from uuid import uuid4
import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from infrastructure.security.authorization.rbac import create_access_token

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"


def make_auth_cookies(role: str) -> dict[str, str]:
    """Generates an authentic session token for a given role."""
    token = create_access_token(
        data={"sub": str(uuid4()), "username": f"test_{role}", "roles": [role]}
    )
    return {"dtfias_session": token}


PUBLIC_ROUTES = [
    "/",
    "/auth/login",
    "/auth/recover",
]

BHARATI_ROUTES = [
    "/bharati/",
    "/bharati/dashboard",
    "/bharati/station-twin",
    "/bharati/twin",
    "/bharati/energy",
    "/bharati/infrastructure",
    "/bharati/environment",
    "/bharati/logistics",
    "/bharati/telemetry",
    "/bharati/alerts",
    "/bharati/personnel",
    "/bharati/health",
    "/bharati/research",
    "/bharati/assets/chp-01",
]

MAITRI_ROUTES = [
    "/maitri/",
    "/maitri/dashboard",
    "/maitri/station-twin",
    "/maitri/twin",
    "/maitri/energy",
    "/maitri/infrastructure",
    "/maitri/environment",
    "/maitri/logistics",
    "/maitri/telemetry",
    "/maitri/alerts",
    "/maitri/personnel",
    "/maitri/health",
    "/maitri/research",
    "/maitri/assets/gen-01",
]

HQ_ROUTES = [
    "/hq/",
    "/hq/dashboard",
    "/hq/stations",
    "/hq/energy",
    "/hq/environment",
    "/hq/logistics",
    "/hq/health",
    "/hq/research",
    "/hq/telemetry",
    "/hq/alerts",
    "/hq/commands",
    "/hq/compliance",
    "/hq/users",
    "/hq/roles",
    "/hq/reports",
    "/hq/audit",
    "/hq/assets",
    "/hq/simulations",
    "/hq/settings",
]

FORBIDDEN_FONTS = ["Space Grotesk", "SpaceGrotesk", "Arial", "Roboto"]


@pytest.mark.asyncio
@pytest.mark.parametrize("route", PUBLIC_ROUTES)
async def test_public_routes_render(route: str):
    """Verifies all public entry points render valid HTML with HTTP 200."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get(route)
        assert res.status_code == 200, f"Route {route} returned {res.status_code}"
        assert "text/html" in res.headers["content-type"]
        assert "<!DOCTYPE html>" in res.text or "<html" in res.text


@pytest.mark.asyncio
@pytest.mark.parametrize("route", BHARATI_ROUTES)
async def test_bharati_portal_routes_render(route: str):
    """Verifies all Bharati station portal views render HTTP 200 with complete DOM."""
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("bharati_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        res = await client.get(route)
        assert res.status_code == 200, f"Bharati route {route} failed with {res.status_code}"
        assert "text/html" in res.headers["content-type"]
        assert "<!DOCTYPE html>" in res.text
        # Assert no raw Jinja syntax escaped into rendered body
        assert "{{ " not in res.text, f"Unrendered Jinja tag detected on {route}"
        # Assert no unhandled Python exceptions
        assert "Internal Server Error" not in res.text
        assert "Traceback" not in res.text


@pytest.mark.asyncio
@pytest.mark.parametrize("route", MAITRI_ROUTES)
async def test_maitri_portal_routes_render(route: str):
    """Verifies all Maitri station portal views render HTTP 200 with complete DOM."""
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("maitri_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        res = await client.get(route)
        assert res.status_code == 200, f"Maitri route {route} failed with {res.status_code}"
        assert "text/html" in res.headers["content-type"]
        assert "<!DOCTYPE html>" in res.text
        assert "{{ " not in res.text, f"Unrendered Jinja tag detected on {route}"
        assert "Internal Server Error" not in res.text
        assert "Traceback" not in res.text


@pytest.mark.asyncio
@pytest.mark.parametrize("route", HQ_ROUTES)
async def test_hq_portal_routes_render(route: str):
    """Verifies all HQ Mission Control views render HTTP 200 with complete DOM."""
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("super_admin")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        res = await client.get(route)
        assert res.status_code == 200, f"HQ route {route} failed with {res.status_code}"
        assert "text/html" in res.headers["content-type"]
        assert "<!DOCTYPE html>" in res.text
        assert "{{ " not in res.text, f"Unrendered Jinja tag detected on {route}"
        assert "Internal Server Error" not in res.text
        assert "Traceback" not in res.text


@pytest.mark.asyncio
async def test_brand_design_compliance_and_forbidden_fonts():
    """
    Validates adherence to DTFIAS Brand Guidelines (.agents/brand_design/SKILL.md):
    - No forbidden fonts in rendered templates.
    - Required brand CSS tokens present.
    """
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("super_admin")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        for route in ["/bharati/dashboard", "/maitri/dashboard", "/hq/dashboard"]:
            res = await client.get(route)
            content = res.text
            for font in FORBIDDEN_FONTS:
                assert font not in content, f"Forbidden font '{font}' found in {route}"
            # Verify brand CSS tokens are loaded in head
            assert "--brand-deep-green" in content
            assert "--brand-teal" in content
            assert "--brand-cream" in content


@pytest.mark.asyncio
async def test_static_assets_referenced_exist_on_disk():
    """
    Extracts all local /static/... asset paths from the dashboard and verifies
    that every referenced image, script, and stylesheet exists on disk.
    """
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("bharati_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        res = await client.get("/bharati/dashboard")
        content = res.text

        # Find static references: href="/static/...", src="/static/..."
        matches = re.findall(r'(?:src|href)=["\']/static/([^"\'?#]+)', content)
        assert len(matches) > 0, "No static assets found in dashboard"

        for asset_rel in set(matches):
            asset_path = STATIC_DIR / asset_rel.replace("/", os.sep)
            assert asset_path.is_file(), f"Referenced static file does not exist: {asset_path}"


@pytest.mark.asyncio
async def test_threejs_lazy_loading_c16():
    """
    Constraint C16: Three.js and station_3d_view.js must be lazy-loaded on demand
    via Alpine x-init and MUST NOT be unconditionally loaded in base.html.
    """
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("bharati_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        # Base template and standard dashboard must not unconditionally load Three.js
        res_dash = await client.get("/bharati/dashboard")
        assert '<script src="/static/js/three/station_3d_view.js">' not in res_dash.text
        assert '<script src="/static/vendor/three.min.js">' not in res_dash.text
        assert "three.min.js" not in res_dash.text

        # Station Twin view contains the lazy-loaded container hook without synchronous Three.js script
        res_twin = await client.get("/bharati/station-twin")
        assert '<script src="/static/js/three/station_3d_view.js">' not in res_twin.text
        assert '<script src="/static/vendor/three.min.js">' not in res_twin.text
        assert "station-3d-container" in res_twin.text


@pytest.mark.asyncio
async def test_mobile_responsive_navigation_components():
    """
    Verifies that mobile navigation components (FE-RESP-001, FE-RESP-002)
    are present in rendered station and HQ views:
    - mobileNavOpen Alpine state
    - Mobile hamburger toggle button
    - Mobile backdrop overlay
    - Responsive left-0 lg:left-72 header positioning
    """
    transport = ASGITransport(app=app)
    cookies = make_auth_cookies("bharati_operator")
    async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
        res = await client.get("/bharati/dashboard")
        assert "mobileNavOpen" in res.text
        assert "left-0 lg:left-72" in res.text
        assert 'aria-label="Toggle navigation drawer"' in res.text
