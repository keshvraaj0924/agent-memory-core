from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])
settings = get_settings()


@router.get("/health", summary="Liveness probe")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@router.get("/ready", summary="Readiness probe")
async def readiness() -> dict[str, str]:
    return {"status": "ready", "service": settings.app_name}
