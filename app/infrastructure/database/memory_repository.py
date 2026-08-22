from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.memory import Memory
from app.domain.enums.memory import MemoryType
from app.infrastructure.database.models import MemoryRecord


class PostgresMemoryRepository:
    """PostgreSQL adapter implementing the memory repository contract."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, memory: Memory) -> Memory:
        record = self._to_record(memory)
        self._session.add(record)
        await self._session.commit()
        return memory

    async def get(self, memory_id: UUID) -> Memory | None:
        result = await self._session.execute(
            select(MemoryRecord).where(MemoryRecord.id == memory_id)
        )
        record = result.scalar_one_or_none()
        return self._to_domain(record) if record is not None else None

    async def update(self, memory: Memory) -> Memory:
        record = await self._session.get(MemoryRecord, memory.id)
        if record is None:
            raise KeyError(f"Memory {memory.id} not found")
        record.content = memory.content
        record.memory_type = memory.memory_type.value
        record.importance = memory.importance
        record.updated_at = memory.updated_at
        record.last_accessed_at = memory.last_accessed_at
        record.access_count = memory.access_count
        await self._session.commit()
        return memory

    async def delete(self, memory_id: UUID) -> bool:
        result = await self._session.execute(
            delete(MemoryRecord).where(MemoryRecord.id == memory_id)
        )
        await self._session.commit()
        return bool(result.rowcount)

    async def list_for_user(self, user_id: str, limit: int = 100) -> list[Memory]:
        result = await self._session.execute(
            select(MemoryRecord)
            .where(MemoryRecord.user_id == user_id)
            .order_by(MemoryRecord.updated_at.desc())
            .limit(limit)
        )
        return [self._to_domain(record) for record in result.scalars().all()]

    @staticmethod
    def _to_record(memory: Memory) -> MemoryRecord:
        return MemoryRecord(
            id=memory.id,
            content=memory.content,
            memory_type=memory.memory_type.value,
            user_id=memory.user_id,
            importance=memory.importance,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
            last_accessed_at=memory.last_accessed_at,
            access_count=memory.access_count,
        )

    @staticmethod
    def _to_domain(record: MemoryRecord) -> Memory:
        now = datetime.now(timezone.utc)
        return Memory(
            id=record.id,
            content=record.content,
            memory_type=MemoryType(record.memory_type),
            user_id=record.user_id,
            importance=record.importance,
            created_at=record.created_at or now,
            updated_at=record.updated_at or now,
            last_accessed_at=record.last_accessed_at or now,
            access_count=record.access_count,
        )
