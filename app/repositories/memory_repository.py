from typing import Protocol
from uuid import UUID

from app.domain.entities.memory import Memory


class MemoryRepository(Protocol):
    async def add(self, memory: Memory) -> Memory: ...

    async def get(self, memory_id: UUID) -> Memory | None: ...
