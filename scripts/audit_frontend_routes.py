import sys
import os
sys.path.insert(0, os.path.abspath("."))

import asyncio
import httpx
import main

async def test_all_routes():
    schema = main.app.openapi()
    paths = schema.get("paths", {})
    client = httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app), base_url="http://test")
    
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
