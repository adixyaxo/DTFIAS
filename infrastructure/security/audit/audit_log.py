# infrastructure/security/audit/audit_log.py
"""
Operational and Security Audit Logging for DTFIAS.
Conforms strictly to Constraint C7:
- Every login, state write, command issuance, and permission denial MUST produce one audit_logs row.
"""
from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from infrastructure.database.postgres.repositories.audit_repository import PostgresAuditRepository


async def record_audit_event(
    session: AsyncSession,
    action: str,
    entity_type: str,
    user_id: UUID | None = None,
    station_id: UUID | None = None,
    entity_id: UUID | None = None,
    old_value: dict[str, Any] | None = None,
    new_value: dict[str, Any] | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    """
    Records an immutable audit log entry.
    Actions include: LOGIN_SUCCESS, LOGIN_FAILED, PERMISSION_DENIED,
    COMMAND_ISSUED, COMMAND_EXECUTED, STATE_WRITE, ROLE_ASSIGNED.
    """
    repo = PostgresAuditRepository(session)
    log_entry = {
        "user_id": user_id,
        "station_id": station_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "old_value": old_value,
        "new_value": new_value,
        "ip_address": ip_address,
        "created_at": datetime.now(timezone.utc),
    }
    return await repo.save(log_entry)


__all__ = ["record_audit_event"]
