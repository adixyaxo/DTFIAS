from fastapi import APIRouter

# In a real app, this would have dependencies=[Depends(require_role("maitri_operator"))]
router = APIRouter(prefix="/maitri", tags=["maitri"])

@router.get("/")
async def maitri_home():
    return {"message": "Welcome to Maitri Portal"}
