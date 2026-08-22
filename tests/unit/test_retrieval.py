from datetime import datetime, timedelta, timezone

from app.domain.entities.memory import Memory
from app.domain.enums.memory import MemoryType
from app.infrastructure.embeddings import HashEmbeddingProvider
from app.services.retrieval import MemoryRetriever, RetrievalWeights


def test_multi_factor_retrieval_prefers_relevant_important_memory() -> None:
    now = datetime.now(timezone.utc)
    relevant = Memory(
        content="User prefers Python for AI projects.",
        memory_type=MemoryType.PREFERENCE,
        user_id="u1",
        importance=0.9,
        last_accessed_at=now,
    )
    unrelated = Memory(
        content="User likes coffee.",
        memory_type=MemoryType.EPISODIC,
        user_id="u1",
        importance=0.2,
        last_accessed_at=now - timedelta(days=120),
    )

    results = MemoryRetriever(embedding_provider=HashEmbeddingProvider(64)).rank(
        [unrelated, relevant], "Python AI"
    )

    assert results[0].memory.id == relevant.id
    assert results[0].score > results[1].score
    assert results[0].semantic_score >= 0.0
    assert results[0].score <= 1.0


def test_retrieval_weights_must_sum_to_one() -> None:
    try:
        RetrievalWeights(
            lexical=0.4,
            semantic=0.4,
            recency=0.2,
            importance=0.2,
            type_match=0.0,
        )
    except ValueError as exc:
        assert "sum to 1.0" in str(exc)
    else:
        raise AssertionError("Expected invalid retrieval weights to be rejected")


def test_retrieval_weights_accept_valid_hybrid_configuration() -> None:
    weights = RetrievalWeights(
        lexical=0.35,
        semantic=0.35,
        recency=0.10,
        importance=0.15,
        type_match=0.05,
    )
    assert weights.semantic == 0.35
