# Agent Memory Core

> Production-grade memory infrastructure for intelligent agents.

[![CI](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml/badge.svg)](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-production-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Agent Memory Core** is a provider-agnostic memory infrastructure service for AI agents. It treats memory as a first-class systems problem: storage, lifecycle, retrieval, ranking, observability, and evaluation are separated into explicit, testable boundaries.

## Current release

**v0.2.0 — Memory Lifecycle + Retrieval Baseline**

The current release provides a complete memory CRUD lifecycle, dependency-injected storage selection, deterministic multi-factor retrieval, PostgreSQL persistence boundaries, Redis infrastructure, database migrations, request correlation, and automated quality checks.

## Architecture

```text
                         ┌──────────────────────┐
                         │      Agent / API      │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │     Memory Service   │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
      ┌───────▼────────┐   ┌────────▼─────────┐  ┌────────▼────────┐
      │ Memory Policy  │   │ Retrieval Engine  │  │ Consolidation   │
      └───────┬────────┘   └────────┬─────────┘  └────────┬────────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │ Repository / Provider Ports   │
                    └───────────────┬───────────────┘
                                    │
                       ┌────────────┼────────────┐
                       ▼            ▼            ▼
                   PostgreSQL     Redis      Vector Store
```

## Memory model

- **Working** — short-lived task state.
- **Episodic** — events and experiences.
- **Semantic** — durable factual knowledge.
- **Preference** — stable user preferences.
- **Procedural** — reusable instructions and behaviors.

Each memory also tracks importance, creation/update time, last access time, and access count so retrieval policy can be measured over time.

## Retrieval baseline

The current retriever deliberately uses deterministic signals rather than pretending lexical overlap is semantic understanding:

```text
R(m, q) = α·lexical_overlap
        + β·recency
        + γ·importance
        + δ·type_match
```

This is a research baseline. The next stage will introduce an embedding provider and compare semantic retrieval against the multi-factor ranking strategy under controlled benchmarks.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/memories` | Create memory |
| GET | `/api/v1/memories/{id}` | Read memory |
| PATCH | `/api/v1/memories/{id}` | Update memory |
| DELETE | `/api/v1/memories/{id}` | Delete memory |
| POST | `/api/v1/memories/search` | Ranked retrieval |
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/ready` | Dependency-aware readiness |

## Production capabilities

- FastAPI HTTP API with versioned endpoints
- Async application and infrastructure boundaries
- Pydantic v2 validation
- SQLAlchemy 2 + async PostgreSQL adapter
- Redis infrastructure adapter
- Configurable in-memory/PostgreSQL backend
- Alembic migration tooling
- Deterministic retrieval baseline with explainable component scores
- Structured JSON logging
- Request correlation via `X-Request-ID`
- Dependency-aware readiness reporting
- Static typing and linting
- Unit tests and retrieval tests
- Docker-based local environment
- GitHub Actions CI
- Architecture Decision Records and research notes

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

For local development, keep `MEMORY_BACKEND=in_memory`. For PostgreSQL-backed operation, set `MEMORY_BACKEND=postgres` and run migrations:

```bash
alembic upgrade head
```

API: `http://localhost:8000`

OpenAPI: `http://localhost:8000/docs`

Readiness: `http://localhost:8000/api/v1/ready`

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy app
```

## Repository layout

```text
app/
  api/             HTTP transport and dependency injection
  core/            settings, logging, middleware, exceptions
  domain/          domain entities and enums
  repositories/    persistence ports
  services/        application use cases and retrieval
  infrastructure/  database and cache adapters
  schemas/         API contracts

tests/
  unit/

docs/
  architecture/
  decisions/
  research/

migrations/         Alembic schema history
.github/workflows/  CI and quality automation
```

## Roadmap

- [x] Repository and architecture foundation
- [x] Memory CRUD lifecycle
- [x] Dependency-injected storage selection
- [x] PostgreSQL persistence adapter
- [x] Alembic migration baseline
- [x] Redis infrastructure adapter
- [x] Deterministic multi-factor retrieval baseline
- [x] Request correlation and readiness checks
- [ ] Embedding provider abstraction + vector retrieval
- [ ] Memory consolidation and deduplication
- [ ] Conflict-aware memory updates
- [ ] Context-budget optimizer
- [ ] Agent-facing SDK
- [ ] Retrieval benchmark suite
- [ ] Production deployment reference

## Design philosophy

The project intentionally separates **domain policy** from **infrastructure implementation**. Storage providers, caches, embedding models, and LLM vendors should be replaceable without rewriting memory semantics.

Every major capability should be measurable. Research claims will be backed by reproducible benchmarks rather than README-only assertions.

## License

Apache-2.0
