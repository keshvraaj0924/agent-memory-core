from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    app_name: str = "agent-memory-core"
    app_version: str = "0.3.0"
    environment: Literal["local", "development", "staging", "production"] = "local"
    debug: bool = False
    log_level: str = "INFO"
    host: str = "0.0.0.0"
    port: int = Field(default=8000, ge=1, le=65535)
    api_prefix: str = "/api/v1"

    memory_backend: Literal["in_memory", "postgres"] = "in_memory"
    retrieval_backend: Literal["hybrid", "semantic"] = "hybrid"
    semantic_embedding_model: str = "BAAI/bge-small-en-v1.5"
    database_url: str = "postgresql+asyncpg://memory:memory@localhost:5432/agent_memory"
    redis_url: str = "redis://localhost:6379/0"
    database_pool_size: int = Field(default=10, ge=1, le=100)
    database_max_overflow: int = Field(default=20, ge=0, le=100)
    cors_origins: str = "http://localhost,http://localhost:3000"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = value.upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed:
            raise ValueError(f"Unsupported log level: {value}")
        return normalized

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
