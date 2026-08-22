import math
import re
from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.entities.memory import Memory
from app.infrastructure.embeddings import HashEmbeddingProvider, cosine_similarity
from app.repositories.embedding import EmbeddingProvider

_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
    "has", "have", "how", "in", "is", "it", "of", "on", "or", "that",
    "the", "this", "to", "was", "what", "when", "where", "which", "who",
    "why", "with", "you", "your",
}


@dataclass(frozen=True, slots=True)
class RetrievalWeights:
    """Weights for explainable hybrid memory ranking."""

    lexical: float = 0.35
    semantic: float = 0.35
    recency: float = 0.10
    importance: float = 0.15
    type_match: float = 0.05

    def __post_init__(self) -> None:
        total = (
            self.lexical
            + self.semantic
            + self.recency
            + self.importance
            + self.type_match
        )
        if not math.isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Retrieval weights must sum to 1.0")


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    memory: Memory
    score: float
    lexical_score: float
    semantic_score: float
    recency_score: float
    importance_score: float
    type_match_score: float


class MemoryRetriever:
    """Deterministic hybrid retrieval baseline with explainable scoring."""

    def __init__(
        self,
        weights: RetrievalWeights | None = None,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        self._weights = weights or RetrievalWeights()
        self._embedding_provider = embedding_provider or HashEmbeddingProvider()

    def rank(
        self,
        memories: list[Memory],
        query: str,
        *,
        memory_type: str | None = None,
        limit: int = 10,
    ) -> list[RetrievalResult]:
        if limit <= 0:
            return []

        query_tokens = _tokenize(query)
        query_embedding = self._embedding_provider.embed(query)
        now = datetime.now(timezone.utc)
        results: list[RetrievalResult] = []

        for memory in memories:
            lexical = _lexical_overlap(query_tokens, _tokenize(memory.content))
            semantic = _normalise_cosine(self._embedding_provider.embed(memory.content), query_embedding)
            age_days = max((now - memory.last_accessed_at).total_seconds() / 86400.0, 0.0)
            recency = math.exp(-age_days / 30.0)
            type_match = 1.0 if memory_type and memory.memory_type.value == memory_type else 0.0
            score = (
                self._weights.lexical * lexical
                + self._weights.semantic * semantic
                + self._weights.recency * recency
                + self._weights.importance * memory.importance
                + self._weights.type_match * type_match
            )
            results.append(
                RetrievalResult(
                    memory=memory,
                    score=score,
                    lexical_score=lexical,
                    semantic_score=semantic,
                    recency_score=recency,
                    importance_score=memory.importance,
                    type_match_score=type_match,
                )
            )

        results.sort(key=lambda item: (item.score, item.memory.created_at), reverse=True)
        return results[:limit]


def _tokenize(value: str) -> set[str]:
    return {token for token in _TOKEN_RE.findall(value.lower()) if token not in _STOP_WORDS}


def _lexical_overlap(query_tokens: set[str], memory_tokens: set[str]) -> float:
    if not query_tokens or not memory_tokens:
        return 0.0
    intersection = len(query_tokens & memory_tokens)
    return intersection / len(query_tokens)


def _normalise_cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    cosine = cosine_similarity(left, right)
    return (cosine + 1.0) / 2.0
