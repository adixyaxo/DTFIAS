# app/routers/hq/commands.py
"""
HQ Commands sub-router.
Invokes HQPortalService to issue and monitor tactical remote commands.
"""
from uuid import UUID
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse
from app.config.templates import templates
from app.dependencies.portals import HQServiceDep
from app.schemas.command import CommandCreate, CommandResponse
from shared.models.enums import CommandType

router = APIRouter()


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
async def hq_issue_command(payload: CommandCreate, service: HQServiceDep):
    # Created by operator (will be extracted from current user session in Phase 4)
    command = await service.issue_command(
        station_id=payload.station_id,
        created_by=payload.station_id,  # Placeholder until JWT session extracted
        command_type=payload.command_type,
        parameters=payload.parameters,
        expires_at=payload.expires_at,
    )
    return command


__all__ = ["router"]
