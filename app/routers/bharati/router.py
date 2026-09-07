from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from shared.constants.stations import get_station_metadata

# In a real app, this would have dependencies=[Depends(require_role("bharati_operator"))]
router = APIRouter(prefix="/bharati", tags=["bharati"])

STATION_INFO = get_station_metadata("bharati")

def render_station(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name=f"station/{name}.html",
        context={
            "station_id": "bharati",
            "station": STATION_INFO,
            "title": f"Bharati - {name.title()}",
        },
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
@router.get("/twin", response_class=HTMLResponse)
async def station_twin(request: Request):
    """Interactive 2.5D station view for Bharati Antarctic Research Station."""
    return templates.TemplateResponse(
        request=request,
        name="bharati/station_twin.html",
        context={
            "title": "Bharati Station — Digital Twin | DTFIAS",
            "station_id": "bharati",
            "station": STATION_INFO,
        },
    )

@router.get("/personnel", response_class=HTMLResponse)
async def bharati_personnel(request: Request):
    return render_station(request, "personnel")

@router.get("/health", response_class=HTMLResponse)
async def bharati_health(request: Request):
    return render_station(request, "health")

@router.get("/research", response_class=HTMLResponse)
async def bharati_research(request: Request):
    return render_station(request, "research")

@router.get("/telemetry", response_class=HTMLResponse)
async def bharati_telemetry(request: Request):
    return render_station(request, "telemetry")

@router.get("/assets/{asset_id}", response_class=HTMLResponse)
async def bharati_asset(request: Request, asset_id: str):
    return templates.TemplateResponse(
        request=request,
        name="station/asset_detail.html",
        context={
            "station_id": "bharati",
            "station": STATION_INFO,
            "asset_id": asset_id,
            "title": f"Bharati - Asset {asset_id}",
        },
    )
