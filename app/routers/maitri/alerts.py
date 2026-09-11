# app/routers/maitri/alerts.py
"""
Maitri Alerts sub-router.
Invokes MaitriPortalService to manage active operational alerts.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import MaitriServiceDep
from shared.constants.stations import get_station_metadata

router = APIRouter()
STATION_INFO = get_station_metadata("maitri")


@router.get("/alerts", response_class=HTMLResponse)
async def maitri_alerts(request: Request, service: MaitriServiceDep):
    active_alerts = await service.get_active_alerts()
    return templates.TemplateResponse(
        request=request,
        name="station/alerts.html",
        context={
            "station_id": "maitri",
            "station": STATION_INFO,
            "title": "Maitri - Alerts",
            "alerts": active_alerts,
        },
    )


__all__ = ["router"]
