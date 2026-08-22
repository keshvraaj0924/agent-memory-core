from uuid import UUID

from app.domain.entities.memory import Memory


class InMemoryMemoryRepository:
    """Deterministic adapter for local development and unit testing."""

    def __init__(self) -> None:
        self._items: dict[UUID, Memory] = {}

    async def add(self, memory: Memory) -> Memory:
        self._items[memory.id] = memory
        return memory

    async def get(self, memory_id: UUID) -> Memory | None:
        return self._items.get(memory_id)
