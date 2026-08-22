from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_memory_service
from app.schemas.memory import (
    MemoryCreate,
    MemoryResponse,
    MemorySearchRequest,
    MemorySearchResult,
    MemoryUpdate,
)
from app.services.memory_service import MemoryService

router = APIRouter(prefix="/memories", tags=["memory"])


@router.post("", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
async def create_memory(
    payload: MemoryCreate,
    service: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    memory = await service.create(payload)
    return MemoryResponse.model_validate(memory)


@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: UUID,
    service: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    memory = await service.get(memory_id)
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return MemoryResponse.model_validate(memory)


@router.patch("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: UUID,
    payload: MemoryUpdate,
    service: MemoryService = Depends(get_memory_service),
) -> MemoryResponse:
    memory = await service.update(memory_id, payload)
    if memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")
    return MemoryResponse.model_validate(memory)


@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_memory(
    memory_id: UUID,
    service: MemoryService = Depends(get_memory_service),
) -> None:
    deleted = await service.delete(memory_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not found")


@router.post("/search", response_model=list[MemorySearchResult])
async def search_memories(
    payload: MemorySearchRequest,
    service: MemoryService = Depends(get_memory_service),
) -> list[MemorySearchResult]:
    results = await service.search(payload)
    return [
        MemorySearchResult(
            memory=MemoryResponse.model_validate(result.memory),
            score=round(result.score, 6),
            lexical_score=round(result.lexical_score, 6),
            semantic_score=round(result.semantic_score, 6),
            recency_score=round(result.recency_score, 6),
            importance_score=round(result.importance_score, 6),
            type_match_score=round(result.type_match_score, 6),
        )
        for result in results
    ]
