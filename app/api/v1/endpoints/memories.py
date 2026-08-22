from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.infrastructure.memory.in_memory_repository import InMemoryMemoryRepository
from app.schemas.memory import MemoryCreate, MemoryResponse
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/memories", tags=["memory"])
_repository = InMemoryMemoryRepository()
_service = MemoryService(_repository)


@router.post("", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(payload: MemoryCreate) -> MemoryResponse:
    memory = await _service.create(payload)
    return MemoryResponse.model_validate(memory)


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(memory_id: UUID) -> MemoryResponse:
    memory = await _service.get(memory_id)
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return MemoryResponse.model_validate(memory)
