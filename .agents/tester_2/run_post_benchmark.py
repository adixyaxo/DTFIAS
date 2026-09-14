"""
Comprehensive Benchmark Runner for DTFIAS FastAPI Application.
Phase 1: Baseline Endpoint Benchmarking.

Discovers and executes live HTTP requests against the Uvicorn server on http://127.0.0.1:8000.
Records TTFB, total response time, size in bytes, HTTP status code, content type, and partial detection.
Saves results to perf_baseline.json matching the exact required schema.
"""
import asyncio
import datetime
import json
import os
import sys
import time
from typing import Any

import httpx

# Ensure project root in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from infrastructure.security.authorization.rbac import create_access_token

BASE_URL = "http://127.0.0.1:8000"
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "perf_baseline.json")

# Generate super admin JWT token for authenticated requests
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

# Test cases: (method, url, route_pattern, is_htmx, extra_kwargs, unauthenticated)
TEST_CASES = [
    # Root
    ("GET", "/", "/", False, {}, False),
    ("GET", "/", "/", True, {}, False),

    # Auth
    ("GET", "/auth/login", "/auth/login", False, {}, True),
    ("GET", "/auth/login", "/auth/login", True, {}, True),
    ("POST", "/auth/login", "/auth/login", False, {"data": {"username": "superadmin@gmail.com", "password": "superadmin123"}}, True),
    ("GET", "/auth/logout", "/auth/logout", False, {}, False),
    ("POST", "/auth/logout", "/auth/logout", False, {}, False),
    ("GET", "/auth/recover", "/auth/recover", False, {}, True),
    ("GET", "/auth/recover", "/auth/recover", True, {}, True),

    # API Users
    ("GET", "/api/users/16921011-8164-4dfa-956e-61b5af59bf4b", "/api/users/{user_id}", False, {}, False),
    ("POST", "/api/users/", "/api/users/", False, {"json": {
        "employee_code": "bench_test_user",
        "full_name": "Benchmark Test User",
        "email": "superadmin@gmail.com",
        "password": "Password123!"
    }}, False),

    # HQ Portal
    ("GET", "/hq/", "/hq/", False, {}, False),
    ("GET", "/hq/", "/hq/", True, {}, False),
    ("GET", "/hq/dashboard", "/hq/dashboard", False, {}, False),
    ("GET", "/hq/dashboard", "/hq/dashboard", True, {}, False),
    ("GET", "/hq/commands", "/hq/commands", False, {}, False),
    ("GET", "/hq/commands", "/hq/commands", True, {}, False),
    ("POST", "/hq/commands", "/hq/commands", False, {"json": {
        "station_id": "274c1092-066e-480f-a3b4-93d6c13a2aa2",
        "command_type": "SYSTEM_CONTROL",
        "parameters": {"action": "diagnostic_ping"}
    }}, False),
    ("GET", "/hq/users", "/hq/users", False, {}, False),
    ("GET", "/hq/users", "/hq/users", True, {}, False),
    ("GET", "/hq/audit", "/hq/audit", False, {}, False),
    ("GET", "/hq/audit", "/hq/audit", True, {}, False),
    ("GET", "/hq/environment", "/hq/environment", False, {}, False),
    ("GET", "/hq/environment", "/hq/environment", True, {}, False),
    ("GET", "/hq/logistics", "/hq/logistics", False, {}, False),
    ("GET", "/hq/logistics", "/hq/logistics", True, {}, False),
    ("GET", "/hq/energy", "/hq/energy", False, {}, False),
    ("GET", "/hq/energy", "/hq/energy", True, {}, False),
    ("GET", "/hq/compliance", "/hq/compliance", False, {}, False),
    ("GET", "/hq/compliance", "/hq/compliance", True, {}, False),
    ("GET", "/hq/assets", "/hq/assets", False, {}, False),
    ("GET", "/hq/assets", "/hq/assets", True, {}, False),
    ("GET", "/hq/telemetry", "/hq/telemetry", False, {}, False),
    ("GET", "/hq/telemetry", "/hq/telemetry", True, {}, False),
    ("GET", "/hq/alerts", "/hq/alerts", False, {}, False),
    ("GET", "/hq/alerts", "/hq/alerts", True, {}, False),
    ("GET", "/hq/stations", "/hq/stations", False, {}, False),
    ("GET", "/hq/stations", "/hq/stations", True, {}, False),
    ("GET", "/hq/health", "/hq/health", False, {}, False),
    ("GET", "/hq/health", "/hq/health", True, {}, False),
    ("GET", "/hq/research", "/hq/research", False, {}, False),
    ("GET", "/hq/research", "/hq/research", True, {}, False),
    ("GET", "/hq/simulations", "/hq/simulations", False, {}, False),
    ("GET", "/hq/simulations", "/hq/simulations", True, {}, False),
    ("GET", "/hq/reports", "/hq/reports", False, {}, False),
    ("GET", "/hq/reports", "/hq/reports", True, {}, False),
    ("GET", "/hq/roles", "/hq/roles", False, {}, False),
    ("GET", "/hq/roles", "/hq/roles", True, {}, False),
    ("GET", "/hq/settings", "/hq/settings", False, {}, False),
    ("GET", "/hq/settings", "/hq/settings", True, {}, False),

    # Bharati Portal
    ("GET", "/bharati/", "/bharati/", False, {}, False),
    ("GET", "/bharati/", "/bharati/", True, {}, False),
    ("GET", "/bharati/dashboard", "/bharati/dashboard", False, {}, False),
    ("GET", "/bharati/dashboard", "/bharati/dashboard", True, {}, False),
    ("GET", "/bharati/energy", "/bharati/energy", False, {}, False),
    ("GET", "/bharati/energy", "/bharati/energy", True, {}, False),
    ("GET", "/bharati/energy/stream", "/bharati/energy/stream", False, {}, False),
    ("GET", "/bharati/alerts", "/bharati/alerts", False, {}, False),
    ("GET", "/bharati/alerts", "/bharati/alerts", True, {}, False),
    ("GET", "/bharati/twin", "/bharati/twin", False, {}, False),
    ("GET", "/bharati/twin", "/bharati/twin", True, {}, False),
    ("GET", "/bharati/station-twin", "/bharati/station-twin", False, {}, False),
    ("GET", "/bharati/station-twin", "/bharati/station-twin", True, {}, False),
    ("GET", "/bharati/infrastructure", "/bharati/infrastructure", False, {}, False),
    ("GET", "/bharati/infrastructure", "/bharati/infrastructure", True, {}, False),
    ("GET", "/bharati/environment", "/bharati/environment", False, {}, False),
    ("GET", "/bharati/environment", "/bharati/environment", True, {}, False),
    ("GET", "/bharati/logistics", "/bharati/logistics", False, {}, False),
    ("GET", "/bharati/logistics", "/bharati/logistics", True, {}, False),
    ("GET", "/bharati/personnel", "/bharati/personnel", False, {}, False),
    ("GET", "/bharati/personnel", "/bharati/personnel", True, {}, False),
    ("GET", "/bharati/health", "/bharati/health", False, {}, False),
    ("GET", "/bharati/health", "/bharati/health", True, {}, False),
    ("GET", "/bharati/research", "/bharati/research", False, {}, False),
    ("GET", "/bharati/research", "/bharati/research", True, {}, False),
    ("GET", "/bharati/telemetry", "/bharati/telemetry", False, {}, False),
    ("GET", "/bharati/telemetry", "/bharati/telemetry", True, {}, False),
    ("GET", "/bharati/assets/c476c0a9-6100-4cf9-8d84-67e47043f1f8", "/bharati/assets/{asset_id}", False, {}, False),
    ("GET", "/bharati/assets/c476c0a9-6100-4cf9-8d84-67e47043f1f8", "/bharati/assets/{asset_id}", True, {}, False),

    # Maitri Portal
    ("GET", "/maitri/", "/maitri/", False, {}, False),
    ("GET", "/maitri/", "/maitri/", True, {}, False),
    ("GET", "/maitri/dashboard", "/maitri/dashboard", False, {}, False),
    ("GET", "/maitri/dashboard", "/maitri/dashboard", True, {}, False),
    ("GET", "/maitri/energy", "/maitri/energy", False, {}, False),
    ("GET", "/maitri/energy", "/maitri/energy", True, {}, False),
    ("GET", "/maitri/energy/stream", "/maitri/energy/stream", False, {}, False),
    ("GET", "/maitri/alerts", "/maitri/alerts", False, {}, False),
    ("GET", "/maitri/alerts", "/maitri/alerts", True, {}, False),
    ("GET", "/maitri/twin", "/maitri/twin", False, {}, False),
    ("GET", "/maitri/twin", "/maitri/twin", True, {}, False),
    ("GET", "/maitri/station-twin", "/maitri/station-twin", False, {}, False),
    ("GET", "/maitri/station-twin", "/maitri/station-twin", True, {}, False),
    ("GET", "/maitri/infrastructure", "/maitri/infrastructure", False, {}, False),
    ("GET", "/maitri/infrastructure", "/maitri/infrastructure", True, {}, False),
    ("GET", "/maitri/environment", "/maitri/environment", False, {}, False),
    ("GET", "/maitri/environment", "/maitri/environment", True, {}, False),
    ("GET", "/maitri/logistics", "/maitri/logistics", False, {}, False),
    ("GET", "/maitri/logistics", "/maitri/logistics", True, {}, False),
    ("GET", "/maitri/personnel", "/maitri/personnel", False, {}, False),
    ("GET", "/maitri/personnel", "/maitri/personnel", True, {}, False),
    ("GET", "/maitri/health", "/maitri/health", False, {}, False),
    ("GET", "/maitri/health", "/maitri/health", True, {}, False),
    ("GET", "/maitri/research", "/maitri/research", False, {}, False),
    ("GET", "/maitri/research", "/maitri/research", True, {}, False),
    ("GET", "/maitri/telemetry", "/maitri/telemetry", False, {}, False),
    ("GET", "/maitri/telemetry", "/maitri/telemetry", True, {}, False),
    ("GET", "/maitri/assets/generator-01", "/maitri/assets/{asset_id}", False, {}, False),
    ("GET", "/maitri/assets/generator-01", "/maitri/assets/{asset_id}", True, {}, False),
]


async def run_single_benchmark(
    client: httpx.AsyncClient,
    method: str,
    url: str,
    route_pattern: str,
    is_htmx: bool,
    extra_kwargs: dict[str, Any],
    unauthenticated: bool,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    async with semaphore:
        headers = {}
        if is_htmx:
            headers["HX-Request"] = "true"

        cookies = {}
        if not unauthenticated:
            headers["Authorization"] = f"Bearer {SUPER_ADMIN_TOKEN}"
            cookies["dtfias_session"] = SUPER_ADMIN_TOKEN

        t_start = time.perf_counter()

        if method == "GET" and url.endswith("/stream"):
            try:
                async with client.stream("GET", url, headers=headers, cookies=cookies) as resp:
                    t_ttfb = time.perf_counter()
                    content = b""
                    async for chunk in resp.aiter_bytes():
                        content += chunk
                        if chunk:
                            break
                    t_total = time.perf_counter()
                    status_code = resp.status_code
                    content_type = resp.headers.get("content-type", "")
            except Exception as e:
                t_ttfb = time.perf_counter()
                t_total = time.perf_counter()
                content = str(e).encode()
                status_code = 500
                content_type = "text/plain"
        else:
            json_data = extra_kwargs.get("json")
            data_payload = extra_kwargs.get("data")
            req = client.build_request(
                method,
                url,
                headers=headers,
                cookies=cookies,
                json=json_data,
                data=data_payload,
            )
            t_start = time.perf_counter()
            try:
                resp = await client.send(req, stream=True)
                t_ttfb = time.perf_counter()
                content = await resp.aread()
                t_total = time.perf_counter()
                status_code = resp.status_code
                content_type = resp.headers.get("content-type", "")
            except Exception as e:
                t_ttfb = time.perf_counter()
                t_total = time.perf_counter()
                content = str(e).encode()
                status_code = 500
                content_type = "text/plain"

        ttfb_ms = round((t_ttfb - t_start) * 1000.0, 2)
        total_time_ms = round((t_total - t_start) * 1000.0, 2)
        size_bytes = len(content)

        # Detect is_partial
        content_str = content.decode("utf-8", errors="ignore").strip().lower()
        if "application/json" in content_type:
            is_partial = True
        elif "text/event-stream" in content_type:
            is_partial = True
        elif "text/html" in content_type:
            if "<!doctype" in content_str or "<html" in content_str:
                is_partial = False
            else:
                is_partial = True
        else:
            is_partial = True

        result = {
            "route": route_pattern,
            "method": method,
            "is_htmx": is_htmx,
            "status_code": status_code,
            "ttfb_ms": ttfb_ms,
            "total_time_ms": total_time_ms,
            "size_bytes": size_bytes,
            "is_partial": is_partial,
            "content_type": content_type,
        }
        print(f"[{result['status_code']}] {method:<4} {route_pattern:<32} (htmx={str(is_htmx):<5}) -> {total_time_ms:>8.2f}ms | {size_bytes:>7}B | partial={is_partial}")
        return result


async def main():
    print(f"Starting DTFIAS Baseline Benchmark on {BASE_URL}...")
    print(f"Total benchmark test cases: {len(TEST_CASES)}")
    semaphore = asyncio.Semaphore(3)

    # Pre-warm connection pool
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=60.0) as client:
        try:
            await client.get("/")
            await client.get("/hq/dashboard", headers={"Authorization": f"Bearer {SUPER_ADMIN_TOKEN}"})
            print("Connection pool pre-warmed successfully.\n")
        except Exception as e:
            print(f"Warning during pre-warm: {e}\n")

    start_time = time.perf_counter()
    iso_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    async with httpx.AsyncClient(base_url=BASE_URL, follow_redirects=False, timeout=60.0) as client:
        tasks = [
            run_single_benchmark(
                client=client,
                method=tc[0],
                url=tc[1],
                route_pattern=tc[2],
                is_htmx=tc[3],
                extra_kwargs=tc[4],
                unauthenticated=tc[5],
                semaphore=semaphore,
            )
            for tc in TEST_CASES
        ]
        results = await asyncio.gather(*tasks)

    elapsed_total = time.perf_counter() - start_time
    print(f"\nAll {len(results)} benchmarks finished in {elapsed_total:.2f}s.")

    # Compute summary statistics
    total_tested = len(results)
    total_time = sum(r["total_time_ms"] for r in results)
    avg_time = round(total_time / total_tested, 2) if total_tested > 0 else 0.0
    total_bytes = sum(r["size_bytes"] for r in results)
    over_1000ms = sum(1 for r in results if r["total_time_ms"] > 1000.0)

    benchmark_data = {
        "timestamp": iso_timestamp,
        "summary": {
            "total_endpoints_tested": total_tested,
            "avg_response_time_ms": avg_time,
            "total_payload_bytes": total_bytes,
            "endpoints_over_1000ms": over_1000ms,
        },
        "endpoints": results,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(benchmark_data, f, indent=2)

    print(f"Results written to {OUTPUT_FILE}")
    print(f"Summary: total={total_tested}, avg={avg_time}ms, bytes={total_bytes}, over_1000ms={over_1000ms}")


if __name__ == "__main__":
    asyncio.run(main())
