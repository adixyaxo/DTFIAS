# app/routers/hq/users.py
"""
HQ Users & Personnel Management sub-router.
Invokes HQPortalService to administer polar operators and credentials.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import HQServiceDep

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
async def hq_users_page(request: Request, service: HQServiceDep):
    users = await service.manage_users()
    return templates.TemplateResponse(
        request=request,
        name="hq/users.html",
        context={
            "station_id": "hq",
            "users": users,
            "title": "NCPOR HQ - Personnel & RBAC",
        },
    )


__all__ = ["router"]
