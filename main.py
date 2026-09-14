from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings, templates
from app.main_router import router as main_router
from app.config.database import Base, engine
from tests.main_tests import test


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run startup checks and create tables
    # await test()
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

# Register Security and Tracing Middleware (Constraints C10, C11)
from app.middleware.request_id import RequestIdMiddleware
from app.middleware.logging import StructuredLoggingMiddleware
from app.middleware.security import SecurityHeadersMiddleware, CSRFProtectionMiddleware

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CSRFProtectionMiddleware)
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Always serve static files via FastAPI (works on both local and Vercel serverless)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "app", "static")), name="static")

app.include_router(main_router)

# Constraint C12: disable template auto-reload in production
if settings.is_production:
    templates.env.auto_reload = False


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
