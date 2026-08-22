from typing import Any

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.core.config import get_settings
from app.infrastructure.cache.redis import RedisCache
from app.infrastructure.database.session import engine

router = APIRouter(tags=["health"])
settings = get_settings()
_redis = RedisCache.from_settings()


@router.get("/health", summary="Liveness probe")
async def health() -> dict[str, str]:
    """Confirm that the application process is alive."""
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@router.get("/ready", summary="Readiness probe")
async def readiness(response: Response) -> dict[str, Any]:
    """Report dependency health and return HTTP 503 when the service is not ready."""
    dependencies: dict[str, str] = {}

    if settings.memory_backend == "postgres":
        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
            dependencies["postgres"] = "ok"
        except Exception:
            dependencies["postgres"] = "unavailable"

    redis_ok = await _redis.ping()
    dependencies["redis"] = "ok" if redis_ok else "unavailable"

    ready = all(value == "ok" for value in dependencies.values())
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ready" if ready else "degraded",
        "service": settings.app_name,
        "version": settings.app_version,
        "dependencies": dependencies,
    }
