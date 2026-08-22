from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.memories import router as memories_router

router = APIRouter()
router.include_router(health_router)
router.include_router(memories_router)
