from typing import Protocol


class EmbeddingProvider(Protocol):
    """Port for text embedding implementations."""

    @property
    def dimension(self) -> int: ...

    def embed(self, text: str) -> tuple[float, ...]: ...
