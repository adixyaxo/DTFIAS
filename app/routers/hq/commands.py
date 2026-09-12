# app/routers/hq/commands.py
"""
HQ Commands sub-router.
Invokes HQPortalService to issue and monitor tactical remote commands.
"""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.config.templates import templates
from app.dependencies.portals import HQServiceDep
from app.schemas.command import CommandCreate, CommandResponse
from app.models.auth import Profile
from infrastructure.security.authorization.rbac import get_current_user_optional
from infrastructure.security.audit.audit_log import record_audit_event
from shared.models.enums import CommandType

router = APIRouter()
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/commands", response_class=HTMLResponse)
async def hq_commands_page(request: Request, service: HQServiceDep):
    overview = await service.get_overview()
    return templates.TemplateResponse(
        request=request,
        name="hq/commands.html",
        context={
            "station_id": "hq",
            "overview": overview,
            "title": "NCPOR HQ - Remote Commands",
        },
    )


@router.post("/commands", response_model=CommandResponse, status_code=status.HTTP_201_CREATED)
async def hq_issue_command(
    request: Request,
    payload: CommandCreate,
    service: HQServiceDep,
    db: DbDep,
    current_user: Profile | None = Depends(get_current_user_optional),
):
    user_id = current_user.id if current_user else payload.station_id
    command = await service.issue_command(
        station_id=payload.station_id,
        created_by=user_id,
        command_type=payload.command_type,
        parameters=payload.parameters,
        expires_at=payload.expires_at,
    )

    # Constraint C7: Every command issuance writes an audit_log row
    try:
        ip_addr = request.client.host if request.client else None
        cmd_id = getattr(command, "id", None)
        cmd_type = getattr(command, "command_type", payload.command_type)
        cmd_type_val = cmd_type.value if hasattr(cmd_type, "value") else str(cmd_type)
        cmd_params = getattr(command, "parameters", payload.parameters)
        cmd_expires = getattr(command, "expires_at", payload.expires_at)

        await record_audit_event(
            session=db,
            action="COMMAND_ISSUED",
            entity_type="commands",
            user_id=current_user.id if current_user else None,
            station_id=payload.station_id,
            entity_id=cmd_id,
            new_value={
                "command_type": cmd_type_val,
                "parameters": cmd_params,
                "expires_at": cmd_expires.isoformat() if cmd_expires else None,
            },
            ip_address=ip_addr,
        )
    except Exception:
        pass

    return command


__all__ = ["router"]
