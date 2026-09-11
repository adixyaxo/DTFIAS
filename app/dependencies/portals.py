# app/dependencies/portals.py
"""
FastAPI dependency providers for Station and HQ Portal Services.
Wires concrete infrastructure repositories into engine portal facades.
"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from infrastructure.database.postgres.repositories import (
    PostgresStationRepository,
    PostgresEnergyRepository,
    PostgresAlertRepository,
    PostgresCommandRepository,
    PostgresAuditRepository,
    PostgresUserRepository,
)
from engine.services.portals.maitri_portal_service import MaitriPortalService
from engine.services.portals.bharati_portal_service import BharatiPortalService
from engine.services.portals.hq_portal_service import HQPortalService

DbDep = Annotated[AsyncSession, Depends(get_db)]


def get_maitri_portal_service(db: DbDep) -> MaitriPortalService:
    """Dependency producing a scoped MaitriPortalService instance."""
    return MaitriPortalService(
        station_repo=PostgresStationRepository(db),
        energy_repo=PostgresEnergyRepository(db),
        alert_repo=PostgresAlertRepository(db),
        command_repo=PostgresCommandRepository(db),
    )


def get_bharati_portal_service(db: DbDep) -> BharatiPortalService:
    """Dependency producing a scoped BharatiPortalService instance."""
    return BharatiPortalService(
        station_repo=PostgresStationRepository(db),
        energy_repo=PostgresEnergyRepository(db),
        alert_repo=PostgresAlertRepository(db),
        command_repo=PostgresCommandRepository(db),
    )


def get_hq_portal_service(db: DbDep) -> HQPortalService:
    """Dependency producing a scoped HQPortalService instance."""
    return HQPortalService(
        station_repo=PostgresStationRepository(db),
        energy_repo=PostgresEnergyRepository(db),
        alert_repo=PostgresAlertRepository(db),
        command_repo=PostgresCommandRepository(db),
        audit_repo=PostgresAuditRepository(db),
        user_repo=PostgresUserRepository(db),
    )


MaitriServiceDep = Annotated[MaitriPortalService, Depends(get_maitri_portal_service)]
BharatiServiceDep = Annotated[BharatiPortalService, Depends(get_bharati_portal_service)]
HQServiceDep = Annotated[HQPortalService, Depends(get_hq_portal_service)]

__all__ = [
    "get_maitri_portal_service",
    "get_bharati_portal_service",
    "get_hq_portal_service",
    "MaitriServiceDep",
    "BharatiServiceDep",
    "HQServiceDep",
]
