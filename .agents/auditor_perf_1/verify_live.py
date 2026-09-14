"""
Independent live measurement script by auditor_perf_1.
Verifies whether endpoints respond with real times, real sizes, and genuine partials.
"""
import asyncio
import time
import sys
import os
import httpx
sys.path.insert(0, os.path.abspath("."))

from infrastructure.security.authorization.rbac import create_access_token

token = create_access_token({
    "sub": "16921011-8164-4dfa-956e-61b5af59bf4b",
    "username": "superadmin@gmail.com",
    "roles": [
        "SUPER_ADMIN",
        "HQ_ADMIN",
        "HQ_OPERATOR",
        "MAITRI_OPERATOR",
        "BHARATI_OPERATOR",
    ],
})

async def main():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000", timeout=60.0, follow_redirects=False) as client:
        endpoints = [
            "/",
            "/hq/environment",
            "/maitri/energy",
            "/bharati/dashboard",
            "/hq/dashboard",
        ]
        cookies = {"dtfias_session": token}
        headers_base = {"Authorization": f"Bearer {token}"}
        print(f"{'Endpoint':<22} {'Mode':<8} {'Status':<6} {'Time (ms)':<10} {'Size (B)':<10} {'Partial':<8} {'Main Container'}")
        print("-" * 75)
        for path in endpoints:
            for hx in [False, True]:
                headers = dict(headers_base)
                if hx:
                    headers["HX-Request"] = "true"
                mode = "HTMX" if hx else "Standard"
                t0 = time.perf_counter()
                r = await client.get(path, headers=headers, cookies=cookies)
                t1 = time.perf_counter()
                elapsed_ms = (t1 - t0) * 1000.0
                text = r.text.lower()
                is_partial = "<!doctype" not in text and "<html" not in text
                has_main = 'id="main-content"' in text or 'id="dashboard_content"' in text
                print(f"{path:<22} {mode:<8} {r.status_code:<6} {elapsed_ms:>9.1f} {len(r.content):>9} {str(is_partial):<8} {has_main}")

if __name__ == "__main__":
    asyncio.run(main())
