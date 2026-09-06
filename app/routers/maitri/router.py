from fastapi import APIRouter
from fastapi.responses import HTMLResponse

# In a real app, this would have dependencies=[Depends(require_role("maitri_operator"))]
router = APIRouter(prefix="/maitri", tags=["maitri"])

@router.get("/", response_class=HTMLResponse)
async def maitri_home():
    return "<div class='text-green-600 font-bold'>Welcome to Maitri Portal (Loaded via HTMX)</div>"
