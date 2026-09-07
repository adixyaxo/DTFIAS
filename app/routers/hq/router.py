from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates

# In a real app, this would have dependencies=[Depends(require_role_in("hq_operator", "hq_admin"))]
router = APIRouter(prefix="/hq", tags=["hq"])

def render_hq(request: Request, name: str):
    return templates.TemplateResponse(request=request, name=f"hq/{name}.html", context={})

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
