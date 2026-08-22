from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.infrastructure.database.memory_repository import PostgresMemoryRepository
from app.infrastructure.database.session import get_session
from app.infrastructure.embeddings import HashEmbeddingProvider, SentenceTransformerEmbeddingProvider
from app.infrastructure.memory.in_memory_repository import InMemoryMemoryRepository
from app.repositories.embedding import EmbeddingProvider
from app.repositories.memory_repository import MemoryRepository
from app.services.memory_service import MemoryService

_settings = get_settings()
_in_memory_repository = InMemoryMemoryRepository()
_hash_embedding_provider = HashEmbeddingProvider()
_sentence_embedding_provider: EmbeddingProvider | None = None


async def get_repository(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[MemoryRepository]:
    if _settings.memory_backend == "postgres":
        yield PostgresMemoryRepository(session)
    else:
        yield _in_memory_repository


def get_embedding_provider() -> EmbeddingProvider:
    global _sentence_embedding_provider

    if _settings.retrieval_backend == "semantic":
        if _sentence_embedding_provider is None:
            _sentence_embedding_provider = SentenceTransformerEmbeddingProvider(
                _settings.semantic_embedding_model
            )
        return _sentence_embedding_provider
    return _hash_embedding_provider


async def get_memory_service(
    repository: MemoryRepository = Depends(get_repository),
    embedding_provider: EmbeddingProvider = Depends(get_embedding_provider),
) -> MemoryService:
    from app.services.retrieval import MemoryRetriever

    retriever = MemoryRetriever(embedding_provider=embedding_provider)
    return MemoryService(repository, retriever=retriever)
