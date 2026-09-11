# app/middleware/logging.py
"""
Structured HTTP access logging middleware for DTFIAS.
Safely logs HTTP operations without ever logging passwords or sensitive tokens (Constraint C6).
"""
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("dtfias.access")


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming requests, status codes, and execution duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", "none")

        response: Response = await call_next(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
        status_code = response.status_code

        # Avoid spamming logs for static vendor assets
        if not request.url.path.startswith("/static/"):
            logger.info(
                f"{request.method} {request.url.path} -> {status_code} ({duration_ms}ms) [id={request_id}]"
            )

        return response


__all__ = ["StructuredLoggingMiddleware"]
