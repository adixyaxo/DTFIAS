import sys
import os
sys.path.insert(0, os.path.abspath("."))

import asyncio
import httpx
from infrastructure.security.authorization.rbac import create_access_token
from app.dependencies.portals import HQServiceDep
import main

# Test token with super_admin permissions
token = create_access_token({
    "sub": "00000000-0000-0000-0000-000000000001",
    "username": "operator",
    "roles": ["super_admin", "hq_admin", "hq_operator", "station_admin", "station_operator", "maitri_operator", "bharati_operator"],
})

# Mock HQPortalService if DB is offline
class MockHQPortalService:
    async def get_overview(self):
        return {
            "total_stations": 2,
            "active_alerts": 3,
            "critical_alerts": 0,
            "overall_status": "NOMINAL",
            "active_souls": 42,
        }

main.app.dependency_overrides[HQServiceDep] = lambda: MockHQPortalService()

async def test_all_routes():
    schema = main.app.openapi()
    paths = schema.get("paths", {})
    client = httpx.AsyncClient(
        transport=httpx.ASGITransport(app=main.app),
        base_url="http://test",
        cookies={"dtfias_session": token},
    )
    
    results = []
    for path, methods in paths.items():
        if "get" in methods:
            test_path = path.replace("{asset_id}", "generator-01").replace("{user_id}", "1")
            try:
                res = await client.get(test_path)
                results.append((test_path, res.status_code, len(res.text)))
            except Exception as e:
                results.append((test_path, "ERROR", str(e)))

    print(f"{'ROUTE':<35} | {'STATUS':<6} | {'BODY LENGTH':<10}")
    print("-" * 58)
    for p, s, l in results:
        print(f"{p:<35} | {str(s):<6} | {str(l):<10}")

asyncio.run(test_all_routes())
