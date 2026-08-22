from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.enums.memory import MemoryType


@dataclass(slots=True)
class Memory:
    """Domain representation of an agent memory independent of persistence."""

    content: str
    memory_type: MemoryType
    user_id: str
    importance: float = 0.5
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    access_count: int = 0

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise ValueError("Memory content must not be empty")
        if not self.user_id.strip():
            raise ValueError("Memory user_id must not be empty")
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("Memory importance must be between 0 and 1")
        if self.access_count < 0:
            raise ValueError("Memory access_count must be non-negative")

    def mark_accessed(self) -> None:
        self.last_accessed_at = datetime.now(timezone.utc)
        self.access_count += 1
