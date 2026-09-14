# app/routers/maitri/dashboard.py
"""
Maitri Dashboard sub-router.
Invokes MaitriPortalService to gather telemetry and microgrid analytics.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import MaitriServiceDep
from shared.constants.stations import get_station_metadata

router = APIRouter()
STATION_INFO = get_station_metadata("maitri")


@router.get("/", response_class=HTMLResponse)
@router.get("/dashboard", response_class=HTMLResponse)
async def maitri_dashboard(request: Request, service: MaitriServiceDep):
    dashboard_data = await service.get_dashboard_data()
    return templates.TemplateResponse(
        request=request,
        name="station/dashboard.html",
        context={
            "station_id": "maitri",
            "station": STATION_INFO,
            "title": "Maitri - Dashboard",
            "dashboard_data": dashboard_data,
            "is_htmx": request.headers.get("HX-Request") == "true",
        },
    )



__all__ = ["router"]
