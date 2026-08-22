from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums.memory import MemoryType


class MemoryCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)
    memory_type: MemoryType
    user_id: str = Field(min_length=1, max_length=256)
    importance: float = Field(default=0.5, ge=0.0, le=1.0)


class MemoryUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1, max_length=10000)
    memory_type: MemoryType | None = None
    importance: float | None = Field(default=None, ge=0.0, le=1.0)


class MemorySearchRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=256)
    query: str = Field(min_length=1, max_length=2000)
    memory_type: MemoryType | None = None
    limit: int = Field(default=10, ge=1, le=100)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    memory_type: MemoryType
    user_id: str
    importance: float
    created_at: datetime
    updated_at: datetime
    last_accessed_at: datetime
    access_count: int


class MemorySearchResult(BaseModel):
    memory: MemoryResponse
    score: float
    lexical_score: float
    recency_score: float
    importance_score: float
    type_match_score: float
