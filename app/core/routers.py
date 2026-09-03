from fastapi import APIRouter

from app.core.health import router as health_router
from app.pipelines.exposures.router import router as exposures_router

router = APIRouter()
router.include_router(health_router)
router.include_router(exposures_router, prefix="/v1")