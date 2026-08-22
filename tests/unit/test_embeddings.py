import pytest

from app.infrastructure.embeddings import HashEmbeddingProvider, cosine_similarity


def test_hash_embedding_is_deterministic() -> None:
    provider = HashEmbeddingProvider(dimension=64)
    first = provider.embed("persistent agent memory")
    second = provider.embed("persistent agent memory")

    assert first == second
    assert len(first) == 64


def test_cosine_similarity_is_normalized() -> None:
    assert cosine_similarity((1.0, 0.0), (1.0, 0.0)) == pytest.approx(1.0)
    assert cosine_similarity((1.0, 0.0), (0.0, 1.0)) == pytest.approx(0.0)


def test_cosine_rejects_mismatched_dimensions() -> None:
    with pytest.raises(ValueError, match="dimensions"):
        cosine_similarity((1.0, 0.0), (1.0,))
