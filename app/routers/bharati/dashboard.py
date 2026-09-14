# app/routers/bharati/dashboard.py
"""
Bharati Dashboard sub-router.
Invokes BharatiPortalService to gather telemetry and microgrid analytics.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import BharatiServiceDep
from shared.constants.stations import get_station_metadata

router = APIRouter()
STATION_INFO = get_station_metadata("bharati")


@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def bharati_dashboard(request: Request, service: BharatiServiceDep):
    dashboard_data = await service.get_dashboard_data()
    return templates.TemplateResponse(
        request=request,
        name="station/dashboard.html",
        context={
            "station_id": "bharati",
            "station": STATION_INFO,
            "title": "Bharati - Dashboard",
            "dashboard_data": dashboard_data,
            "is_htmx": request.headers.get("HX-Request") == "true",
        },
    )


__all__ = ["router"]
