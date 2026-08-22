from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.memory import MemoryType


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    memory_type: MemoryType
    user_id: str = Field(min_length=1, max_length=256)
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    memory_type: MemoryType
    user_id: str
    importance: float
    created_at: datetime
    updated_at: datetime
