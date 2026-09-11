# app/routers/hq/dashboard.py
"""
HQ Mission Control Dashboard sub-router.
Invokes HQPortalService to aggregate multi-station operations.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import HQServiceDep

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def hq_dashboard(request: Request, service: HQServiceDep):
    overview = await service.get_overview()
    return templates.TemplateResponse(
        request=request,
        name="hq/dashboard.html",
        context={
            "station_id": "hq",
            "overview": overview,
            "title": "NCPOR HQ - Mission Control",
        },
    )


__all__ = ["router"]
