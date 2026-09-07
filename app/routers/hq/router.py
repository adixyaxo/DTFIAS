from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates

# In a real app, this would have dependencies=[Depends(require_role_in("hq_operator", "hq_admin"))]
router = APIRouter(prefix="/hq", tags=["hq"])

def render_hq(request: Request, name: str):
    return templates.TemplateResponse(request=request, name=f"hq/{name}.html", context={"station_id": "hq"})

@router.get("/", response_class=HTMLResponse)
async def hq_home(request: Request):
    return render_hq(request, "dashboard")

@router.get("/environment", response_class=HTMLResponse)
async def hq_environment(request: Request):
    return render_hq(request, "environment")

@router.get("/logistics", response_class=HTMLResponse)
async def hq_logistics(request: Request):
    return render_hq(request, "logistics")

@router.get("/energy", response_class=HTMLResponse)
async def hq_energy(request: Request):
    return render_hq(request, "energy")

@router.get("/compliance", response_class=HTMLResponse)
async def hq_compliance(request: Request):
    return render_hq(request, "compliance")

@router.get("/assets", response_class=HTMLResponse)
async def hq_assets(request: Request):
    return render_hq(request, "assets")

@router.get("/audit", response_class=HTMLResponse)
async def hq_audit(request: Request):
    return render_hq(request, "audit")

@router.get("/users", response_class=HTMLResponse)
async def hq_users(request: Request):
    return render_hq(request, "users")

@router.get("/telemetry", response_class=HTMLResponse)
async def hq_telemetry(request: Request):
    return render_hq(request, "telemetry")

@router.get("/alerts", response_class=HTMLResponse)
async def hq_alerts(request: Request):
    return render_hq(request, "alerts")

@router.get("/stations", response_class=HTMLResponse)
async def hq_stations(request: Request):
    return render_hq(request, "stations")

@router.get("/commands", response_class=HTMLResponse)
async def hq_commands(request: Request):
    return render_hq(request, "commands")

@router.get("/health", response_class=HTMLResponse)
async def hq_health(request: Request):
    return render_hq(request, "health")

@router.get("/research", response_class=HTMLResponse)
async def hq_research(request: Request):
    return render_hq(request, "research")

@router.get("/simulations", response_class=HTMLResponse)
async def hq_simulations(request: Request):
    return render_hq(request, "simulations")

@router.get("/reports", response_class=HTMLResponse)
async def hq_reports(request: Request):
    return render_hq(request, "reports")

@router.get("/roles", response_class=HTMLResponse)
async def hq_roles(request: Request):
    return render_hq(request, "roles")

@router.get("/settings", response_class=HTMLResponse)
async def hq_settings(request: Request):
    return render_hq(request, "settings")
