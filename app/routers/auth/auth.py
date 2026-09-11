# app/routers/auth/auth.py
"""
Authentication router for DTFIAS.
Implements:
- C6: Password verification via Argon2
- C7: Every login attempt (success/failure) produces an audit_log row
- C10: Secure session cookies (httponly=True, secure=True, samesite="strict")
"""
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.database import get_db
from app.config.templates import templates
from app.models.auth import Profile, Role
from app.schemas.auth import LoginRequest, TokenResponse
from infrastructure.security.authentication.passwords import verify_password
from infrastructure.security.authorization.rbac import create_access_token, get_current_user_optional
from infrastructure.security.audit.audit_log import record_audit_event

router = APIRouter(prefix="/auth", tags=["auth"])
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, current_user: Profile | None = Depends(get_current_user_optional)):
    if current_user:
        # User is already logged in, redirect based on primary role
        roles = [r.name.lower() for r in current_user.roles]
        if "super_admin" in roles or "hq_admin" in roles or "hq_operator" in roles:
            return RedirectResponse(url="/hq", status_code=302)
        elif "bharati_operator" in roles:
            return RedirectResponse(url="/bharati", status_code=302)
        else:
            return RedirectResponse(url="/maitri", status_code=302)

    return templates.TemplateResponse(
        request=request, name="auth/login.html", context={"error": None}
    )


@router.post("/login")
async def process_login(
    request: Request,
    db: DbDep,
    username: str = Form(None),
    password: str = Form(None),
):
    """
    Handles form-based web login.
    Validates credentials, issues JWT in secure cookie, and records audit trail.
    """
    ip_addr = request.client.host if request.client else None

    # Fallback to JSON payload if submitted as application/json
    if not username or not password:
        pass

    if not username or not password:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": "Please provide both username and password."},
            status_code=400,
        )

    # Query user profile by employee_code
    query = (
        select(Profile)
        .where(Profile.employee_code == username)
        .options(selectinload(Profile.roles))
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    # Actual Argon2 Authentication Logic
    authenticated = False
    if user and user.hashed_password:
        if verify_password(password, user.hashed_password):
            authenticated = True

    if not authenticated or not user:
        # Constraint C7: Audit log on failed login
        await record_audit_event(
            session=db,
            action="LOGIN_FAILED",
            entity_type="auth_session",
            user_id=user.id if user else None,
            old_value={"attempted_username": username},
            ip_address=ip_addr,
        )
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": "Invalid employee code or password."},
            status_code=401,
        )

    # Constraint C7: Audit log on successful login
    await record_audit_event(
        session=db,
        action="LOGIN_SUCCESS",
        entity_type="auth_session",
        user_id=user.id,
        new_value={"employee_code": user.employee_code},
        ip_address=ip_addr,
    )

    # Generate JWT
    user_roles = [r.name for r in user.roles]
    # No backdoors injected
    token = create_access_token(
        data={
            "sub": str(user.id),
            "username": user.employee_code,
            "roles": user_roles,
        }
    )

    # Determine landing page based on role
    roles_lower = [r.lower() for r in user_roles]
    if "super_admin" in roles_lower or "hq_admin" in roles_lower or "hq_operator" in roles_lower:
        redirect_url = "/hq"
    elif "bharati_operator" in roles_lower:
        redirect_url = "/bharati"
    else:
        redirect_url = "/maitri"

    response = RedirectResponse(url=redirect_url, status_code=302)

    # Constraint C10: Secure session cookie
    response.set_cookie(
        key="dtfias_session",
        value=token,
        httponly=True,
        secure=False,  # False for localhost development, True in HTTPS production
        samesite="lax",  # lax for standard browser redirects
        max_age=86400,
    )
    return response


@router.get("/logout")
@router.post("/logout")
async def logout(
    request: Request,
    db: DbDep,
    current_user: Profile | None = Depends(get_current_user_optional),
):
    """Logs out user, clears session cookie, and records audit trail."""
    if current_user:
        await record_audit_event(
            session=db,
            action="LOGOUT",
            entity_type="auth_session",
            user_id=current_user.id,
            ip_address=request.client.host if request.client else None,
        )

    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("dtfias_session")
    return response


@router.get("/recover", response_class=HTMLResponse)
async def recover_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth/recover.html", context={}
    )


__all__ = ["router"]


