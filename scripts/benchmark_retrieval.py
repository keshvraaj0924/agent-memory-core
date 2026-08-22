"""Run a small deterministic retrieval benchmark for local regression checks."""

from datetime import datetime, timezone

from app.domain.entities.memory import Memory
from app.domain.enums.memory import MemoryType
from app.infrastructure.embeddings import HashEmbeddingProvider
from app.services.retrieval import MemoryRetriever


DATASET = [
    (
        "What Python version does the user prefer?",
        "Python 3.12 is the preferred runtime for current AI projects.",
        "python ai projects",
    ),
    (
        "Which deployment environment is preferred?",
        "The service should be containerized with Docker for repeatable deployments.",
        "docker deployments",
    ),
    (
        "What type of memory stores reusable agent procedures?",
        "Procedural memory stores reusable instructions and agent behaviors.",
        "procedural instructions",
    ),
]


def main() -> None:
    retriever = MemoryRetriever(embedding_provider=HashEmbeddingProvider())
    memories = [
        Memory(
            content=content,
            memory_type=MemoryType.SEMANTIC,
            user_id="benchmark-user",
            importance=0.8,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            last_accessed_at=datetime.now(timezone.utc),
        )
        for _, content, _ in DATASET
    ]

    print("query,expected_top1,actual_top1,top1_score")
    for query, expected, _ in DATASET:
        result = retriever.rank(memories, query, limit=1)[0]
        print(f'"{query}","{expected}","{result.memory.content}",{result.score:.6f}')


if __name__ == "__main__":
    main()
