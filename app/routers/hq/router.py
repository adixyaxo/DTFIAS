from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from infrastructure.security.authorization.rbac import require_role_in

from app.routers.hq.dashboard import router as dashboard_router
from app.routers.hq.commands import router as commands_router
from app.routers.hq.users import router as users_router
from app.routers.hq.audit import router as audit_router

# Constraint C5: Role guard is mounted on the APIRouter level
router = APIRouter(
    prefix="/hq",
    tags=["hq"],
    dependencies=[Depends(require_role_in("hq_operator", "hq_admin", "super_admin"))],
)


# Include domain modular sub-routers
router.include_router(dashboard_router)
router.include_router(commands_router)
router.include_router(users_router)
router.include_router(audit_router)

def render_hq(request: Request, name: str):
    return templates.TemplateResponse(request=request, name=f"hq/{name}.html", context={"station_id": "hq"})

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

@router.get("/telemetry", response_class=HTMLResponse)
async def hq_telemetry(request: Request):
    return render_hq(request, "telemetry")

@router.get("/alerts", response_class=HTMLResponse)
async def hq_alerts(request: Request):
    return render_hq(request, "alerts")

@router.get("/stations", response_class=HTMLResponse)
async def hq_stations(request: Request):
    return render_hq(request, "stations")


@router.get("/health", response_class=HTMLResponse)
async def hq_health(request: Request):
    return render_hq(request, "health")

@router.get("/research", response_class=HTMLResponse)
async def hq_research(request: Request):
    return render_hq(request, "research")

from fastapi.responses import RedirectResponse

@router.get("/simulations", response_class=HTMLResponse)
async def hq_simulations(request: Request):
    return render_hq(request, "simulations")

@router.get("/reports", response_class=RedirectResponse)
async def hq_reports(request: Request):
    return RedirectResponse(url="/hq/compliance", status_code=301)

@router.get("/roles", response_class=RedirectResponse)
async def hq_roles(request: Request):
    return RedirectResponse(url="/hq/users", status_code=301)

@router.get("/settings", response_class=HTMLResponse)
async def hq_settings(request: Request):
    return render_hq(request, "settings")
