# app/routers/bharati/alerts.py
"""
Bharati Alerts sub-router.
Invokes BharatiPortalService to manage active operational alerts.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import BharatiServiceDep
from shared.constants.stations import get_station_metadata

router = APIRouter()
STATION_INFO = get_station_metadata("bharati")


@router.get("/alerts", response_class=HTMLResponse)
async def bharati_alerts(request: Request, service: BharatiServiceDep):
    active_alerts = await service.get_active_alerts()
    return templates.TemplateResponse(
        request=request,
        name="station/alerts.html",
        context={
            "station_id": "bharati",
            "station": STATION_INFO,
            "title": "Bharati - Alerts",
            "alerts": active_alerts,
        },
    )


__all__ = ["router"]
