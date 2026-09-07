from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.config.templates import templates

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth/login.html", context={}
    )

@router.post("/login")
async def process_login():
    return {"message": "Login processing goes here"}

@router.get("/recover", response_class=HTMLResponse)
async def recover_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth/recover.html", context={}
    )

@router.get("/logout")
@router.post("/logout")
async def logout():
    return RedirectResponse(url="/auth/login", status_code=302)

