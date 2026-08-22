from uuid import UUID

from app.domain.entities.memory import Memory
from app.repositories.memory_repository import MemoryRepository
from app.schemas.memory import MemoryCreate


class MemoryService:
    """Application service for memory lifecycle operations."""

    def __init__(self, repository: MemoryRepository) -> None:
        self._repository = repository

    async def create(self, payload: MemoryCreate) -> Memory:
        memory = Memory(
            content=payload.content,
            memory_type=payload.memory_type,
            user_id=payload.user_id,
            importance=payload.importance,
        )
        return await self._repository.add(memory)

    async def get(self, memory_id: UUID) -> Memory | None:
        return await self._repository.get(memory_id)
