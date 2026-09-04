from fastapi import APIRouter

# In a real app, this would have dependencies=[Depends(require_role("bharati_operator"))]
router = APIRouter(prefix="/bharati", tags=["bharati"])

@router.get("/")
async def bharati_home():
    return {"message": "Welcome to Bharati Portal"}
