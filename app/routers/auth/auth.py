from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login():
    return {"message": "Login page goes here"}

@router.post("/login")
async def process_login():
    return {"message": "Login processing goes here"}

