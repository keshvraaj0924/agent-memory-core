from redis.asyncio import Redis, from_url

from app.core.config import get_settings


class RedisCache:
    """Small infrastructure adapter for health checks and future caching policy."""

    def __init__(self, client: Redis) -> None:
        self._client = client

    @classmethod
    def from_settings(cls) -> "RedisCache":
        settings = get_settings()
        return cls(from_url(settings.redis_url, decode_responses=True))

    async def ping(self) -> bool:
        try:
            return bool(await self._client.ping())
        except Exception:
            return False

    async def close(self) -> None:
        await self._client.aclose()
