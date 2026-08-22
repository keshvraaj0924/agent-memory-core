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

    async def update(self, memory: Memory) -> Memory:
        if memory.id not in self._items:
            raise KeyError(f"Memory {memory.id} not found")
        self._items[memory.id] = memory
        return memory

    async def delete(self, memory_id: UUID) -> bool:
        return self._items.pop(memory_id, None) is not None

    async def list_for_user(self, user_id: str, limit: int = 100) -> list[Memory]:
        items = [memory for memory in self._items.values() if memory.user_id == user_id]
        items.sort(key=lambda memory: memory.updated_at, reverse=True)
        return items[:limit]
