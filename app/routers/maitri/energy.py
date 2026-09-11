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

router = APIRouter()
STATION_INFO = get_station_metadata("maitri")
MAITRI_STATION_ID = UUID("00000000-0000-0000-0000-000000000001") # Dummy UUID, in reality would use actual ID from DB


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
    """
    async def event_generator():
        last_time = None
        while True:
            if await request.is_disconnected():
                break
            
            # Fetch latest reading
            # In a real app we'd fetch actual station ID dynamically from DB
            reading = await service.get_latest_reading()
            
            if reading and getattr(reading, "time", None) != last_time:
                last_time = getattr(reading, "time", None)
                
                # Format payload
                data = {
                    "battery_soc_pct": getattr(reading, "battery_soc_pct", None),
                    "generation_kw": getattr(reading, "generation_kw", None),
                    "consumption_kw": getattr(reading, "consumption_kw", None),
                    "time": last_time.isoformat() if last_time else None
                }
                
                yield f"data: {json.dumps(data)}\n\n"
            
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


__all__ = ["router"]
