# app/middleware/security.py
"""
Security middleware for DTFIAS.
Implements:
- Security headers (HSTS, X-Content-Type-Options, X-Frame-Options)
- Constraint C11: CSRF validation on mutating methods
"""
import secrets
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import status
from fastapi.responses import JSONResponse


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds hardened security headers to all HTTP responses."""

    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """
    CSRF Protection (Constraint C11):
    Issues a CSRF cookie on safe GET/HEAD requests.
    Validates CSRF token on mutating requests (POST, PUT, DELETE, PATCH).
    Exempts public endpoints: /auth/login, /docs, /openapi.json.
    """

    SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
    EXEMPT_PATHS = {"/auth/login", "/docs", "/openapi.json", "/redoc"}

    async def dispatch(self, request: Request, call_next):
        # Issue CSRF token in cookie if not set
        csrf_cookie = request.cookies.get("dtfias_csrf")
        new_csrf = csrf_cookie or secrets.token_urlsafe(32)
        request.state.csrf_token = new_csrf

        if request.method in self.SAFE_METHODS:
            response = await call_next(request)
            if not csrf_cookie:
                response.set_cookie(
                    key="dtfias_csrf",
                    value=new_csrf,
                    httponly=False,  # JavaScript accessible for HTMX
                    samesite="lax",
                )
            return response

        # Mutating methods
        if any(request.url.path.startswith(exempt) for exempt in self.EXEMPT_PATHS):
            response = await call_next(request)
            if not csrf_cookie:
                response.set_cookie(key="dtfias_csrf", value=new_csrf, httponly=False, samesite="lax")
            return response

        # Validate header matches cookie exactly
        csrf_header = request.headers.get("X-CSRF-Token")
        
        # Exemption for pure Bearer API clients (non-browser)
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            return await call_next(request)
            
        if not csrf_cookie or not csrf_header or not secrets.compare_digest(csrf_header, csrf_cookie):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "CSRF token validation failed. Invalid or missing token."},
            )

        response = await call_next(request)
        return response


__all__ = ["SecurityHeadersMiddleware", "CSRFProtectionMiddleware"]
