# app/routers/hq/audit.py
"""
HQ Audit sub-router.
Invokes HQPortalService to inspect immutable system audit trail (Constraint C7).
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import HQServiceDep

router = APIRouter()


@router.get("/audit", response_class=HTMLResponse)
async def hq_audit_page(request: Request, service: HQServiceDep):
    audit_logs = await service.view_audit(limit=100)
    return templates.TemplateResponse(
        request=request,
        name="hq/audit.html",
        context={
            "station_id": "hq",
            "audit_logs": audit_logs,
            "title": "NCPOR HQ - Audit & Compliance",
        },
    )


__all__ = ["router"]
