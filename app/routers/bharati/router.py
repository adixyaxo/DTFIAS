from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates

# In a real app, this would have dependencies=[Depends(require_role("bharati_operator"))]
router = APIRouter(prefix="/bharati", tags=["bharati"])

def render_station(request: Request, name: str):
    return templates.TemplateResponse(
        request=request, name=f"station/{name}.html", context={"station_id": "bharati", "title": f"Bharati - {name.title()}"}
    )

@router.get("/", response_class=HTMLResponse)
async def bharati_home(request: Request):
    return render_station(request, "dashboard")

@router.get("/energy", response_class=HTMLResponse)
async def bharati_energy(request: Request):
    return render_station(request, "energy")

@router.get("/infrastructure", response_class=HTMLResponse)
async def bharati_infrastructure(request: Request):
    return render_station(request, "infrastructure")

@router.get("/environment", response_class=HTMLResponse)
async def bharati_environment(request: Request):
    return render_station(request, "environment")

@router.get("/logistics", response_class=HTMLResponse)
async def bharati_logistics(request: Request):
    return render_station(request, "logistics")

@router.get("/alerts", response_class=HTMLResponse)
async def bharati_alerts(request: Request):
    return render_station(request, "alerts")

@router.get("/station-twin", response_class=HTMLResponse)
async def station_twin(request: Request):
    """Interactive 2.5D station view for Bharati Antarctic Research Station."""
    return templates.TemplateResponse(
        request=request,
        name="bharati/station_twin.html",
        context={"title": "Bharati Station — Digital Twin | DTFIAS", "station_id": "bharati"},
    )
