"""
Unit & Integration Tests for Phase 3.5 SPA-Style HTMX Navigation.
Verifies:
1. base.html defines hx-boost="true", hx-target="#main-content", hx-select="#main-content", hx-swap="innerHTML", hx-push-url="true".
2. base.html wires Alpine.js tree re-initialization (Alpine.initTree) on htmx:afterSwap / htmx:after:swap.
3. dashboard.html declares stable <main id="main-content"> and portal-sidebar-wrapper.
4. partial.html delivers partial fragment enclosed in <main id="main-content"> with id="dashboard_content".
5. station_twin.html (Bharati 2.5D twin) wraps in <main id="main-content"> and uses hx-boost="false" on the return link.
6. Navigation requests with HX-Request: true return lightweight partial fragments across portals (Maitri, Bharati, HQ).
"""
import pathlib
from uuid import uuid4
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from infrastructure.security.authorization.rbac import create_access_token

REPO_ROOT = pathlib.Path(__file__).parent.parent.parent
BASE_HTML_PATH = REPO_ROOT / "app" / "templates" / "layouts" / "base.html"
DASHBOARD_HTML_PATH = REPO_ROOT / "app" / "templates" / "layouts" / "dashboard.html"
PARTIAL_HTML_PATH = REPO_ROOT / "app" / "templates" / "layouts" / "partial.html"
STATION_TWIN_HTML_PATH = REPO_ROOT / "app" / "templates" / "bharati" / "station_twin.html"


def make_test_token(role: str = "hq_operator") -> dict[str, str]:
    user_id = str(uuid4())
    token = create_access_token(
        data={"sub": user_id, "username": f"user_{role}", "roles": [role]}
    )
    return {"dtfias_session": token}


class TestSPANavigationTemplates:
    """Validates structural markup and HTMX attributes in template layouts."""

    def test_base_html_defines_htmx_spa_attributes(self):
        content = BASE_HTML_PATH.read_text(encoding="utf-8")
        assert 'hx-boost="true"' in content
        assert 'hx-target="#main-content"' in content
        assert 'hx-select="#main-content"' in content
        assert 'hx-swap="innerHTML"' in content
        assert 'hx-push-url="true"' in content
        assert 'id="main-content"' in content

    def test_base_html_wires_alpine_reinit_and_state_sync(self):
        content = BASE_HTML_PATH.read_text(encoding="utf-8")
        assert "Alpine.initTree" in content
        assert "htmx:afterSwap" in content
        assert "htmx:after:swap" in content
        assert "syncNavigationState" in content

    def test_dashboard_html_has_stable_container_and_sidebar_wrapper(self):
        content = DASHBOARD_HTML_PATH.read_text(encoding="utf-8")
        assert 'id="main-content"' in content
        assert 'id="dashboard_content"' in content
        assert 'id="portal-sidebar-wrapper"' in content

    def test_partial_html_has_canonical_main_content_and_oob_sidebar(self):
        content = PARTIAL_HTML_PATH.read_text(encoding="utf-8")
        assert '<main id="main-content"' in content
        assert 'id="dashboard_content"' in content
        assert 'id="portal-sidebar-wrapper"' in content
        assert 'hx-swap-oob="true"' in content

    def test_station_twin_html_has_main_content_and_back_button(self):
        content = STATION_TWIN_HTML_PATH.read_text(encoding="utf-8")
        assert '<main id="main-content"' in content
        assert 'hx-boost="false"' in content
        assert 'href="/hq/dashboard"' in content


class TestSPANavigationEndpoints:
    """Verifies that HX-Request: true produces partial fragments without full page reloads."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "url,role",
        [
            ("/hq/", "hq_operator"),
            ("/hq/energy", "hq_operator"),
            ("/hq/environment", "hq_operator"),
            ("/maitri/", "maitri_operator"),
            ("/maitri/energy", "maitri_operator"),
            ("/bharati/", "bharati_operator"),
            ("/bharati/energy", "bharati_operator"),
        ],
    )
    async def test_htmx_request_returns_partial_fragment_with_main_content(self, url: str, role: str):
        transport = ASGITransport(app=app)
        cookies = make_test_token(role)
        async with AsyncClient(transport=transport, base_url="http://test", cookies=cookies) as client:
            # Full standard page request
            res_full = await client.get(url)
            assert res_full.status_code == 200
            assert "<!DOCTYPE html>" in res_full.text or "<html" in res_full.text
            full_len = len(res_full.content)

            # HTMX SPA partial request
            res_partial = await client.get(url, headers={"HX-Request": "true"})
            assert res_partial.status_code == 200
            assert "<!DOCTYPE html>" not in res_partial.text
            assert "<html" not in res_partial.text
            assert 'id="main-content"' in res_partial.text
            assert 'id="dashboard_content"' in res_partial.text
            partial_len = len(res_partial.content)

            # Assert substantial payload reduction
            assert partial_len < full_len
            reduction = (full_len - partial_len) / full_len * 100
            assert reduction > 50, f"Expected >50% reduction for {url}, got {reduction:.1f}%"
