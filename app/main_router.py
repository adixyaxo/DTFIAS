from app.routers.maitri.router import router as maitri_router
from app.routers.bharati.router import router as bharati_router
from app.routers.hq.router import router as hq_router
from app.routers.auth.auth import router as auth_router
from app.routers.auth.user import router as user_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(maitri_router)
router.include_router(bharati_router)
router.include_router(hq_router)
router.include_router(auth_router)
router.include_router(user_router)