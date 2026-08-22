from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.infrastructure.database.memory_repository import PostgresMemoryRepository
from app.infrastructure.database.session import get_session
from app.infrastructure.memory.in_memory_repository import InMemoryMemoryRepository
from app.repositories.memory_repository import MemoryRepository
from app.services.memory_service import MemoryService

_settings = get_settings()
_in_memory_repository = InMemoryMemoryRepository()


async def get_repository(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[MemoryRepository]:
    if _settings.memory_backend == "postgres":
        yield PostgresMemoryRepository(session)
    else:
        yield _in_memory_repository


async def get_memory_service(
    repository: MemoryRepository = Depends(get_repository),
) -> MemoryService:
    return MemoryService(repository)
