# Changelog

All notable changes to this project are documented here.

## [0.2.0] - 2026-08-22

### Added

- Complete memory create/read/update/delete lifecycle.
- Dependency-injected in-memory and PostgreSQL repository selection.
- Deterministic multi-factor retrieval baseline using lexical relevance, recency, importance, and memory-type match.
- Retrieval component scores for explainability and benchmarking.
- PostgreSQL access metadata for memory reads and access counts.
- Alembic migration configuration and initial memories migration.
- Redis health/cache infrastructure adapter.
- Request correlation with `X-Request-ID`.
- Dependency-aware readiness reporting.
- Retrieval and API lifecycle test coverage.

### Changed

- Runtime configuration is explicit for memory backend, database pools, Redis, CORS, and API version.
- Project README now documents the research baseline and production roadmap.

## [0.1.0] - 2026-08-22

### Added

- Enterprise-oriented project structure.
- FastAPI application with versioned API.
- Health and readiness endpoints.
- Memory domain taxonomy and entity.
- Memory application service and repository port.
- Deterministic local memory adapter.
- PostgreSQL session/model/repository boundary.
- Pydantic API contracts.
- Structured logging and typed configuration.
- Docker and Docker Compose infrastructure.
- Ruff, MyPy, pytest, and GitHub Actions CI.
- Security, contribution, architecture, and research documentation.
