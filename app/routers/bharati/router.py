from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.config.templates import templates

# In a real app, this would have dependencies=[Depends(require_role("bharati_operator"))]
router = APIRouter(prefix="/bharati", tags=["bharati"])


@router.get("/", response_class=HTMLResponse)
async def bharati_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="layouts/base.html",
        context={"title": "Bharati Portal — DTFIAS"},
    )


@router.get("/station-twin", response_class=HTMLResponse)
async def station_twin(request: Request):
    """Interactive 2.5D station view for Bharati Antarctic Research Station."""
    return templates.TemplateResponse(
        request=request,
        name="bharati/station_twin.html",
        context={"title": "Bharati Station — Digital Twin | DTFIAS"},
    )
