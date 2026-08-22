from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.memory import Memory
from app.domain.enums.memory import MemoryType
from app.infrastructure.database.models import MemoryRecord


class PostgresMemoryRepository:
    """PostgreSQL adapter implementing the memory repository contract."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, memory: Memory) -> Memory:
        record = MemoryRecord(
            id=memory.id,
            content=memory.content,
            memory_type=memory.memory_type.value,
            user_id=memory.user_id,
            importance=memory.importance,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
        )
        self._session.add(record)
        await self._session.commit()
        return memory

    async def get(self, memory_id: UUID) -> Memory | None:
        result = await self._session.execute(
            select(MemoryRecord).where(MemoryRecord.id == memory_id)
        )
        record = result.scalar_one_or_none()
        if record is None:
            return None

        return Memory(
            id=record.id,
            content=record.content,
            memory_type=MemoryType(record.memory_type),
            user_id=record.user_id,
            importance=record.importance,
            created_at=record.created_at or datetime.now(timezone.utc),
            updated_at=record.updated_at or datetime.now(timezone.utc),
        )
