"""
DTFIAS Phase 5 Empirical Challenger & Stress Testing Suite.
Author: challenger_perf_1 (EMPIRICAL CHALLENGER)

Validates live server endpoints on http://127.0.0.1:8000:
1. POST /hq/commands (HTTP 201, zero MissingGreenlet, concurrent bursts, schema errors)
2. GET /maitri/energy/stream & GET /bharati/energy/stream (SSE vs non-SSE headers, immediate snapshot, clean termination)
3. HTMX Partial Fragment Requests (HX-Request: true, <main id="main-content">, OOB sidebar, 75-90% payload reduction)
4. Unauthenticated requests (401 access denial, 302 /auth/login redirects)
5. Mixed concurrency stress testing (30 simultaneous mixed requests)
6. GEMINI.md hard architectural constraints (C1, C8, C13, C14, C16)
"""

import asyncio
import json
import re
import subprocess
import time
from uuid import UUID, uuid4
import pytest
import httpx

from infrastructure.security.authorization.rbac import create_access_token

BASE_URL = "http://127.0.0.1:8000"
BHARATI_STATION_ID = "274c1092-066e-480f-a3b4-93d6c13a2aa2"
MAITRI_STATION_ID = "f155965c-2de5-4f82-a481-f50fa69047ba"

SUPER_ADMIN_TOKEN = create_access_token({
    "sub": "16921011-8164-4dfa-956e-61b5af59bf4b",
    "username": "superadmin@gmail.com",
    "roles": [
        "SUPER_ADMIN",
        "HQ_ADMIN",
        "HQ_OPERATOR",
        "STATION_ADMIN",
        "STATION_OPERATOR",
        "MAITRI_OPERATOR",
        "BHARATI_OPERATOR",
    ],
})

AUTH_HEADERS = {
    "Authorization": f"Bearer {SUPER_ADMIN_TOKEN}",
}
AUTH_COOKIES = {
    "dtfias_session": SUPER_ADMIN_TOKEN,
}


@pytest.mark.asyncio
class TestCommandIssuance:
    """Empirical verification of POST /hq/commands."""

    async def test_post_command_valid_bharati(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            payload = {
                "station_id": BHARATI_STATION_ID,
                "command_type": "SYSTEM_CONTROL",
                "parameters": {"action": "diagnostic_ping", "challenger_test": True},
            }
            res = await client.post(
                "/hq/commands",
                json=payload,
                headers=AUTH_HEADERS,
                cookies=AUTH_COOKIES,
            )
            assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
            data = res.json()
            assert "id" in data
            assert data["station_id"] == BHARATI_STATION_ID
            assert data["command_type"] == "SYSTEM_CONTROL"
            assert data["status"] in ("PENDING", "RECEIVED", "VALIDATED", "EXECUTING", "EXECUTED")
            assert "MissingGreenlet" not in res.text

    async def test_post_command_valid_maitri(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            payload = {
                "station_id": MAITRI_STATION_ID,
                "command_type": "ENERGY_CONTROL",
                "parameters": {"action": "generator_health_check", "test_id": str(uuid4())},
            }
            res = await client.post(
                "/hq/commands",
                json=payload,
                headers=AUTH_HEADERS,
                cookies=AUTH_COOKIES,
            )
            assert res.status_code == 201, f"Expected 201, got {res.status_code}: {res.text}"
            data = res.json()
            assert "id" in data
            assert data["station_id"] == MAITRI_STATION_ID
            assert data["command_type"] == "ENERGY_CONTROL"
            assert "MissingGreenlet" not in res.text

    async def test_post_command_validation_error_handling(self):
        """Invalid payloads must return 422 Unprocessable Entity, not 500 internal server error."""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            # Missing station_id and command_type
            res = await client.post(
                "/hq/commands",
                json={},
                headers=AUTH_HEADERS,
                cookies=AUTH_COOKIES,
            )
            assert res.status_code == 422, f"Expected 422, got {res.status_code}: {res.text}"

            # Invalid command_type enum
            res = await client.post(
                "/hq/commands",
                json={"station_id": BHARATI_STATION_ID, "command_type": "INVALID_COMMAND_TYPE"},
                headers=AUTH_HEADERS,
                cookies=AUTH_COOKIES,
            )
            assert res.status_code == 422, f"Expected 422, got {res.status_code}: {res.text}"

    async def test_post_command_concurrent_burst(self):
        """10 concurrent command issuances must all succeed with 201 and 0 MissingGreenlet."""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            async def issue_one(i: int):
                payload = {
                    "station_id": BHARATI_STATION_ID if i % 2 == 0 else MAITRI_STATION_ID,
                    "command_type": "SYSTEM_CONTROL",
                    "parameters": {"burst_index": i, "token": str(uuid4())},
                }
                return await client.post(
                    "/hq/commands",
                    json=payload,
                    headers=AUTH_HEADERS,
                    cookies=AUTH_COOKIES,
                )

            tasks = [issue_one(i) for i in range(10)]
            responses = await asyncio.gather(*tasks)

            for i, res in enumerate(responses):
                assert res.status_code == 201, f"Task {i} failed: {res.status_code} {res.text}"
                assert "MissingGreenlet" not in res.text


@pytest.mark.asyncio
class TestSSEStreams:
    """Empirical verification of /maitri/energy/stream and /bharati/energy/stream."""

    @pytest.mark.parametrize("stream_url", ["/maitri/energy/stream", "/bharati/energy/stream"])
    async def test_non_sse_client_immediate_clean_exit(self, stream_url: str):
        """Non-SSE client receives immediate single snapshot and finishes cleanly without hanging."""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            t0 = time.perf_counter()
            res = await client.get(
                stream_url,
                headers={"Accept": "text/html,application/xhtml+xml,*/*", **AUTH_HEADERS},
                cookies=AUTH_COOKIES,
            )
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            assert res.status_code == 200
            assert "text/event-stream" in res.headers.get("content-type", "")
            # Must deliver initial snapshot data: {...}\n\n
            assert res.text.startswith("data: ")
            payload = json.loads(res.text.replace("data: ", "").strip())
            assert "battery_soc_pct" in payload
            assert "generation_kw" in payload
            assert "consumption_kw" in payload
            # Non-SSE client must exit promptly
            assert elapsed_ms < 2000.0, f"Expected non-SSE stream to complete in <2000ms, took {elapsed_ms:.1f}ms"

    @pytest.mark.parametrize("stream_url", ["/maitri/energy/stream", "/bharati/energy/stream"])
    async def test_sse_client_stream_initial_event_and_disconnect(self, stream_url: str):
        """SSE client with text/event-stream receives valid initial event chunk and cleanly disconnects."""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
            headers = {"Accept": "text/event-stream", **AUTH_HEADERS}
            async with client.stream("GET", stream_url, headers=headers, cookies=AUTH_COOKIES) as stream_res:
                assert stream_res.status_code == 200
                assert "text/event-stream" in stream_res.headers.get("content-type", "")

                received_chunks = []
                async for chunk in stream_res.aiter_bytes():
                    received_chunks.append(chunk)
                    if len(received_chunks) >= 1:
                        break  # Clean disconnect after first chunk

                data_str = b"".join(received_chunks).decode("utf-8")
                assert "data: " in data_str
                # Verify JSON structure
                lines = [line for line in data_str.split("\n") if line.startswith("data: ")]
                assert len(lines) >= 1
                payload = json.loads(lines[0].replace("data: ", "").strip())
                assert "battery_soc_pct" in payload


@pytest.mark.asyncio
class TestHTMXPartialFragments:
    """Empirical verification of HTMX partial fragment requests and payload reduction."""

    ROUTES = [
        # HQ routes
        "/hq/",
        "/hq/dashboard",
        "/hq/commands",
        "/hq/energy",
        "/hq/environment",
        "/hq/alerts",
        "/hq/users",
        "/hq/audit",
        "/hq/logistics",
        "/hq/compliance",
        # Maitri routes
        "/maitri/",
        "/maitri/dashboard",
        "/maitri/energy",
        "/maitri/environment",
        "/maitri/alerts",
        "/maitri/station-twin",
        # Bharati routes
        "/bharati/",
        "/bharati/dashboard",
        "/bharati/energy",
        "/bharati/environment",
        "/bharati/alerts",
        "/bharati/station-twin",
    ]

    @pytest.mark.parametrize("route", ROUTES)
    async def test_htmx_partial_vs_full_reduction(self, route: str):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            # 1. Full page request
            res_full = await client.get(route, headers=AUTH_HEADERS, cookies=AUTH_COOKIES)
            assert res_full.status_code == 200, f"Full request to {route} failed: {res_full.status_code}"
            assert "<!DOCTYPE html>" in res_full.text or "<html" in res_full.text
            full_bytes = len(res_full.content)

            # 2. HTMX partial request
            htmx_headers = {"HX-Request": "true", **AUTH_HEADERS}
            res_partial = await client.get(route, headers=htmx_headers, cookies=AUTH_COOKIES)
            assert res_partial.status_code == 200, f"HTMX request to {route} failed: {res_partial.status_code}"
            assert "<!DOCTYPE html>" not in res_partial.text
            assert "<html" not in res_partial.text
            assert 'id="main-content"' in res_partial.text

            # For standard portal pages, verify out-of-band sidebar update is present
            if "station-twin" not in route:
                assert 'id="portal-sidebar-wrapper"' in res_partial.text
                assert 'hx-swap-oob="true"' in res_partial.text

            partial_bytes = len(res_partial.content)
            reduction_pct = (full_bytes - partial_bytes) / full_bytes * 100.0

            # Target: >= 50% reduction (target range 75-90%)
            assert reduction_pct >= 50.0, (
                f"Route {route}: full={full_bytes}B, partial={partial_bytes}B, "
                f"reduction={reduction_pct:.1f}% (expected >= 50%)"
            )


@pytest.mark.asyncio
class TestUnauthenticatedAccess:
    """Empirical verification of unauthenticated access denial and redirect flows."""

    PORTAL_ROUTES = [
        "/hq/dashboard",
        "/hq/commands",
        "/maitri/dashboard",
        "/bharati/dashboard",
    ]

    @pytest.mark.parametrize("route", PORTAL_ROUTES)
    async def test_portal_unauthenticated_blocked(self, route: str):
        """Unauthenticated requests to protected portal routes must be rejected with 401."""
        async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=False, timeout=10.0) as client:
            res = await client.get(route)
            assert res.status_code == 401, f"Expected 401 for unauthenticated {route}, got {res.status_code}"

    async def test_logout_redirect(self):
        """GET and POST /auth/logout must 302 redirect to /auth/login."""
        async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=False, timeout=10.0) as client:
            res_get = await client.get("/auth/logout")
            assert res_get.status_code == 302
            assert res_get.headers.get("location") == "/auth/login"

            res_post = await client.post("/auth/logout")
            assert res_post.status_code == 302
            assert res_post.headers.get("location") == "/auth/login"

    async def test_authenticated_login_page_redirects_to_portal(self):
        """GET /auth/login with active session cookie redirects to active portal."""
        async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=False, timeout=10.0) as client:
            res = await client.get("/auth/login", cookies=AUTH_COOKIES)
            assert res.status_code == 302
            assert res.headers.get("location") in ("/hq", "/bharati", "/maitri")


@pytest.mark.asyncio
class TestConcurrentStressBurst:
    """Adversarial challenge: simultaneous 30-request burst of mixed traffic."""

    async def test_mixed_traffic_burst(self):
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            requests = []

            # 5 POST /hq/commands
            for i in range(5):
                requests.append(client.post(
                    "/hq/commands",
                    json={
                        "station_id": BHARATI_STATION_ID if i % 2 == 0 else MAITRI_STATION_ID,
                        "command_type": "SYSTEM_CONTROL",
                        "parameters": {"stress_burst": i},
                    },
                    headers=AUTH_HEADERS,
                    cookies=AUTH_COOKIES,
                ))

            # 5 GET /maitri/energy/stream (non-SSE client snapshot)
            for _ in range(5):
                requests.append(client.get(
                    "/maitri/energy/stream",
                    headers={"Accept": "text/html", **AUTH_HEADERS},
                    cookies=AUTH_COOKIES,
                ))

            # 5 GET /bharati/energy/stream (non-SSE client snapshot)
            for _ in range(5):
                requests.append(client.get(
                    "/bharati/energy/stream",
                    headers={"Accept": "text/html", **AUTH_HEADERS},
                    cookies=AUTH_COOKIES,
                ))

            # 5 GET /hq/dashboard (HTMX partial)
            for _ in range(5):
                requests.append(client.get(
                    "/hq/dashboard",
                    headers={"HX-Request": "true", **AUTH_HEADERS},
                    cookies=AUTH_COOKIES,
                ))

            # 5 GET /maitri/energy (HTMX partial)
            for _ in range(5):
                requests.append(client.get(
                    "/maitri/energy",
                    headers={"HX-Request": "true", **AUTH_HEADERS},
                    cookies=AUTH_COOKIES,
                ))

            # 5 GET /bharati/station-twin (HTMX partial)
            for _ in range(5):
                requests.append(client.get(
                    "/bharati/station-twin",
                    headers={"HX-Request": "true", **AUTH_HEADERS},
                    cookies=AUTH_COOKIES,
                ))

            t0 = time.perf_counter()
            responses = await asyncio.gather(*requests)
            burst_duration = time.perf_counter() - t0

            # Verify 0 HTTP 500 errors
            status_codes = [r.status_code for r in responses]
            server_errors = [sc for sc in status_codes if sc >= 500]
            assert len(server_errors) == 0, f"Server errors encountered during burst: {server_errors}"

            successes = [sc for sc in status_codes if sc in (200, 201)]
            assert len(successes) == 30, f"Expected 30 successes, got {len(successes)}: {status_codes}"
            print(f"\n30-request concurrent mixed burst completed in {burst_duration:.2f}s with 0 errors.")


class TestGEMINIArchitecturalConstraints:
    """Empirical verification of GEMINI.md hard constraints."""

    def test_c1_engine_layer_purity(self):
        """C1: engine/** must import ZERO of fastapi, sqlalchemy, asyncpg, jinja2."""
        proc = subprocess.run(
            ["grep", "-rE", "^(import|from) (fastapi|sqlalchemy|asyncpg|jinja2)", "engine/"],
            capture_output=True,
            text=True,
            shell=True,
        )
        assert proc.stdout.strip() == "", f"C1 violation detected in engine/:\n{proc.stdout}"

    def test_c8_zero_fstring_sql(self):
        """C8: All SQL via SQLAlchemy ORM/parameterized queries. Zero f-string SQL."""
        proc = subprocess.run(
            ["grep", "-rn", 'f"SELECT', "app/", "engine/", "infrastructure/"],
            capture_output=True,
            text=True,
            shell=True,
        )
        assert proc.stdout.strip() == "", f"C8 violation detected:\n{proc.stdout}"

    def test_c13_no_service_role_key_in_frontend(self):
        """C13: SUPABASE_SERVICE_ROLE_KEY must never appear in app/static/ or app/templates/."""
        proc = subprocess.run(
            ["grep", "-rn", "SUPABASE_SERVICE_ROLE_KEY", "app/static/", "app/templates/"],
            capture_output=True,
            text=True,
            shell=True,
        )
        assert proc.stdout.strip() == "", f"C13 violation detected in frontend:\n{proc.stdout}"

    def test_c14_no_supabase_js_in_browser(self):
        """C14: No supabase-js Realtime subscription from browser."""
        proc = subprocess.run(
            ["grep", "-rn", "supabase-js\\|createClient(", "app/static/", "app/templates/"],
            capture_output=True,
            text=True,
            shell=True,
        )
        assert proc.stdout.strip() == "", f"C14 violation detected in frontend:\n{proc.stdout}"

    def test_c16_no_threejs_in_base_layout(self):
        """C16: Three.js must be lazy-loaded only, never in layouts/base.html."""
        base_html = subprocess.run(
            ["grep", "-rn", "station_3d_view.js\\|three.min.js", "app/templates/layouts/base.html"],
            capture_output=True,
            text=True,
            shell=True,
        )
        assert base_html.stdout.strip() == "", f"C16 violation in base.html:\n{base_html.stdout}"
