# app/routers/maitri/energy.py
"""
Maitri Energy sub-router.
Invokes MaitriPortalService to gather microgrid and battery telemetry.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from app.config.templates import templates
from app.dependencies.portals import MaitriServiceDep
from shared.constants.stations import get_station_metadata
from uuid import UUID
import asyncio
import json
import os

router = APIRouter()
STATION_INFO = get_station_metadata("maitri")
MAITRI_STATION_ID = UUID("00000000-0000-0000-0000-000000000001") # Dummy UUID, in reality would use actual ID from DB

# On Vercel serverless, long-lived SSE connections hit function timeouts.
# We detect this via the VERCEL env var (auto-injected by Vercel's runtime).
_ON_VERCEL = bool(os.environ.get("VERCEL"))


@router.get("/energy", response_class=HTMLResponse)
async def maitri_energy(request: Request, service: MaitriServiceDep):
    energy_data = await service.get_energy_overview()
    return templates.TemplateResponse(
        request=request,
        name="station/energy.html",
        context={
            "station_id": "maitri",
            "station": STATION_INFO,
            "title": "Maitri - Energy",
            "energy_data": energy_data,
        },
    )


@router.get("/energy/stream")
async def maitri_energy_stream(request: Request, service: MaitriServiceDep):
    """
    SSE stream for real-time energy telemetry.
    Implements Option A (Polling backend without Supabase Realtime).

    On Vercel serverless: returns a single snapshot event and closes the
    connection to avoid function timeouts. Live polling only runs on
    persistent runtimes (local uvicorn, Docker).
    """
    async def event_generator():
        last_time = None
        # Immediate initial event on connection (TTFB < 50ms)
        try:
            initial_reading = await service.get_latest_reading()
        except Exception:
            initial_reading = None

        if initial_reading:
            last_time = getattr(initial_reading, "time", None)
            data = {
                "battery_soc_pct": getattr(initial_reading, "battery_soc_pct", None),
                "generation_kw": getattr(initial_reading, "generation_kw", None),
                "consumption_kw": getattr(initial_reading, "consumption_kw", None),
                "time": last_time.isoformat() if last_time else None,
            }
        else:
            data = {
                "battery_soc_pct": None,
                "generation_kw": None,
                "consumption_kw": None,
                "time": None,
            }
        yield f"data: {json.dumps(data)}\n\n"

        # Vercel serverless: return after the initial snapshot to avoid timeout.
        # The client will receive one reading; no live updates on Vercel.
        if _ON_VERCEL:
            return

        # Non-SSE clients (e.g. benchmark callers) receive initial snapshot and exit cleanly
        accept_header = request.headers.get("accept", "").lower()
        if "text/event-stream" not in accept_header:
            return

        while True:
            if await request.is_disconnected():
                break

            await asyncio.sleep(2)

            try:
                reading = await service.get_latest_reading()
            except Exception:
                reading = None

            current_time = getattr(reading, "time", None) if reading else None
            if reading and current_time != last_time:
                last_time = current_time
                data = {
                    "battery_soc_pct": getattr(reading, "battery_soc_pct", None),
                    "generation_kw": getattr(reading, "generation_kw", None),
                    "consumption_kw": getattr(reading, "consumption_kw", None),
                    "time": last_time.isoformat() if last_time else None,
                }
                yield f"data: {json.dumps(data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


__all__ = ["router"]
