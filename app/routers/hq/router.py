from fastapi import APIRouter

# In a real app, this would have dependencies=[Depends(require_role_in("hq_operator", "hq_admin"))]
router = APIRouter(prefix="/hq", tags=["hq"])

@router.get("/")
async def hq_home():
    return {"message": "Welcome to HQ Portal"}
