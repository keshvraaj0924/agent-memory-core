from datetime import datetime, timezone
from uuid import UUID

from app.domain.entities.memory import Memory
from app.repositories.memory_repository import MemoryRepository
from app.schemas.memory import MemoryCreate, MemorySearchRequest, MemoryUpdate
from app.services.retrieval import MemoryRetriever, RetrievalResult


class MemoryService:
    """Application service coordinating memory lifecycle and retrieval."""

    def __init__(
        self,
        repository: MemoryRepository,
        retriever: MemoryRetriever | None = None,
    ) -> None:
        self._repository = repository
        self._retriever = retriever or MemoryRetriever()

    async def create(self, payload: MemoryCreate) -> Memory:
        memory = Memory(
            content=payload.content,
            memory_type=payload.memory_type,
            user_id=payload.user_id,
            importance=payload.importance,
        )
        return await self._repository.add(memory)

    async def get(self, memory_id: UUID) -> Memory | None:
        memory = await self._repository.get(memory_id)
        if memory is not None:
            memory.mark_accessed()
            await self._repository.update(memory)
        return memory

    async def update(self, memory_id: UUID, payload: MemoryUpdate) -> Memory | None:
        memory = await self._repository.get(memory_id)
        if memory is None:
            return None

        if payload.content is not None:
            memory.content = payload.content
        if payload.memory_type is not None:
            memory.memory_type = payload.memory_type
        if payload.importance is not None:
            memory.importance = payload.importance
        memory.updated_at = datetime.now(timezone.utc)
        return await self._repository.update(memory)

    async def delete(self, memory_id: UUID) -> bool:
        return await self._repository.delete(memory_id)

    async def search(self, request: MemorySearchRequest) -> list[RetrievalResult]:
        memories = await self._repository.list_for_user(request.user_id, limit=1000)
        memory_type = request.memory_type.value if request.memory_type else None
        return self._retriever.rank(
            memories,
            request.query,
            memory_type=memory_type,
            limit=request.limit,
        )
