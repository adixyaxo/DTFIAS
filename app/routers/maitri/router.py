from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from shared.constants.stations import get_station_metadata

# In a real app, this would have dependencies=[Depends(require_role("maitri_operator"))]
router = APIRouter(prefix="/maitri", tags=["maitri"])

STATION_INFO = get_station_metadata("maitri")

def render_station(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name=f"station/{name}.html",
        context={
            "station_id": "maitri",
            "station": STATION_INFO,
            "title": f"Maitri - {name.title()}",
        },
    )

@router.get("/", response_class=HTMLResponse)
async def maitri_home(request: Request):
    return render_station(request, "dashboard")

@router.get("/energy", response_class=HTMLResponse)
async def maitri_energy(request: Request):
    return render_station(request, "energy")

@router.get("/infrastructure", response_class=HTMLResponse)
async def maitri_infrastructure(request: Request):
    return render_station(request, "infrastructure")

@router.get("/environment", response_class=HTMLResponse)
async def maitri_environment(request: Request):
    return render_station(request, "environment")

@router.get("/logistics", response_class=HTMLResponse)
async def maitri_logistics(request: Request):
    return render_station(request, "logistics")

@router.get("/alerts", response_class=HTMLResponse)
async def maitri_alerts(request: Request):
    return render_station(request, "alerts")

@router.get("/station-twin", response_class=HTMLResponse)
@router.get("/twin", response_class=HTMLResponse)
async def maitri_twin(request: Request):
    """Maitri currently uses the 2D SVG version of the twin (not 2.5D like Bharati)."""
    return render_station(request, "twin")

@router.get("/personnel", response_class=HTMLResponse)
async def maitri_personnel(request: Request):
    return render_station(request, "personnel")

@router.get("/health", response_class=HTMLResponse)
async def maitri_health(request: Request):
    return render_station(request, "health")

@router.get("/research", response_class=HTMLResponse)
async def maitri_research(request: Request):
    return render_station(request, "research")

@router.get("/telemetry", response_class=HTMLResponse)
async def maitri_telemetry(request: Request):
    return render_station(request, "telemetry")

@router.get("/assets/{asset_id}", response_class=HTMLResponse)
async def maitri_asset(request: Request, asset_id: str):
    return templates.TemplateResponse(
        request=request,
        name="station/asset_detail.html",
        context={
            "station_id": "maitri",
            "station": STATION_INFO,
            "asset_id": asset_id,
            "title": f"Maitri - Asset {asset_id}",
        },
    )
