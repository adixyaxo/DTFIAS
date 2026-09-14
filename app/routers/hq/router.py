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

def render_hq(request: Request, name: str, title: str | None = None):
    page_title = title or f"HQ - {name.replace('_', ' ').title()}"
    is_htmx = request.headers.get("HX-Request") == "true"
    return templates.TemplateResponse(
        request=request,
        name=f"hq/{name}.html",
        context={"station_id": "hq", "title": page_title, "is_htmx": is_htmx},
    )

@router.get("/environment", response_class=HTMLResponse)
async def hq_environment(request: Request):
    return render_hq(request, "environment", "HQ - Geospatial & Environment")

@router.get("/logistics", response_class=HTMLResponse)
async def hq_logistics(request: Request):
    return render_hq(request, "logistics", "HQ - Logistics & Supply")

@router.get("/energy", response_class=HTMLResponse)
async def hq_energy(request: Request):
    return render_hq(request, "energy", "HQ - Microgrid & Energy")

@router.get("/compliance", response_class=HTMLResponse)
async def hq_compliance(request: Request):
    return render_hq(request, "compliance", "HQ - Compliance & Reports")

@router.get("/assets", response_class=HTMLResponse)
async def hq_assets(request: Request):
    return render_hq(request, "assets", "HQ - Asset Infrastructure")

@router.get("/telemetry", response_class=HTMLResponse)
async def hq_telemetry(request: Request):
    return render_hq(request, "telemetry", "HQ - Telemetry Streams")

@router.get("/alerts", response_class=HTMLResponse)
async def hq_alerts(request: Request):
    return render_hq(request, "alerts", "HQ - Alert Triage")

@router.get("/stations", response_class=HTMLResponse)
async def hq_stations(request: Request):
    return render_hq(request, "stations", "HQ - Station Registry")


@router.get("/health", response_class=HTMLResponse)
async def hq_health(request: Request):
    return render_hq(request, "health", "HQ - Health & Readiness")

@router.get("/research", response_class=HTMLResponse)
async def hq_research(request: Request):
    return render_hq(request, "research", "HQ - Research Operations")

@router.get("/simulations", response_class=HTMLResponse)
async def hq_simulations(request: Request):
    return render_hq(request, "simulations", "HQ - Protocol Simulations")

@router.get("/reports", response_class=HTMLResponse)
async def hq_reports(request: Request):
    return render_hq(request, "reports", "HQ - Operational Reports")

@router.get("/roles", response_class=HTMLResponse)
async def hq_roles(request: Request):
    return render_hq(request, "roles", "HQ - Roles & Permissions Matrix")

@router.get("/settings", response_class=HTMLResponse)
async def hq_settings(request: Request):
    return render_hq(request, "settings", "HQ - System Settings")
