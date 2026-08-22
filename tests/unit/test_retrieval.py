from datetime import datetime, timedelta, timezone

from app.domain.entities.memory import Memory
from app.domain.enums.memory import MemoryType
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

    results = MemoryRetriever().rank([unrelated, relevant], "Python AI")

    assert results[0].memory.id == relevant.id
    assert results[0].score > results[1].score


def test_retrieval_weights_must_sum_to_one() -> None:
    try:
        RetrievalWeights(lexical=0.5, recency=0.2, importance=0.2, type_match=0.2)
    except ValueError as exc:
        assert "sum to 1.0" in str(exc)
    else:
        raise AssertionError("Expected invalid retrieval weights to be rejected")
