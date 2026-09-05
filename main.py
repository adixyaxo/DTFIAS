from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config import settings, templates
from app.main_router import router as main_router
from app.config.database import Base, engine
from tests.main_tests import test

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (run once)
    await test()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(main_router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="layouts/base.html", context={"title": "DTFIAS Home"}
    )

