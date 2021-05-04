from fastapi import APIRouter

from .oauth import router as oauth_router


router = APIRouter(prefix="/api")

router.include_router(oauth_router)
