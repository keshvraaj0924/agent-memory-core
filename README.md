# Agent Memory Core

> Production-grade memory infrastructure for intelligent agents.

[![CI](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml/badge.svg)](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-production-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Agent Memory Core** is a provider-agnostic memory infrastructure service for AI agents. It treats memory as a first-class systems problem: storage, lifecycle, retrieval, ranking, observability, and evaluation are separated into explicit, testable boundaries.

## Current release

**v0.3.0 — Hybrid Semantic Retrieval Foundation**

The current release adds an embedding provider boundary, deterministic local vector embeddings, optional Sentence Transformers support, and explainable hybrid retrieval that combines lexical, semantic, recency, importance, and memory-type signals.

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
              │             ┌───────▼────────┐            │
              │             │ Embedding Port │            │
              │             └───────┬────────┘            │
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

## Retrieval model

The current hybrid retriever exposes every scoring component so ranking decisions are inspectable:

```text
R(m, q) = α·lexical
        + β·semantic
        + γ·recency
        + δ·importance
        + ε·type_priority
```

Default weights:

```text
lexical      0.35
semantic     0.35
recency      0.10
importance   0.15
type         0.05
```

The default local embedding implementation is deterministic and intentionally lightweight for tests and development. A model-backed Sentence Transformers provider is available through the optional `semantic` dependency set.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/memories` | Create memory |
| GET | `/api/v1/memories/{id}` | Read memory |
| PATCH | `/api/v1/memories/{id}` | Update memory |
| DELETE | `/api/v1/memories/{id}` | Delete memory |
| POST | `/api/v1/memories/search` | Ranked hybrid retrieval |
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/ready` | Dependency-aware readiness |

Search responses include the overall score plus lexical, semantic, recency, importance, and type-match components for observability and evaluation.

## Production capabilities

- FastAPI HTTP API with versioned endpoints
- Async application and infrastructure boundaries
- Pydantic v2 validation
- SQLAlchemy 2 + async PostgreSQL adapter
- Redis infrastructure adapter
- Configurable in-memory/PostgreSQL backend
- Configurable retrieval/embedding backend
- Alembic migration tooling
- Hybrid retrieval with explainable score decomposition
- Deterministic local embedding baseline
- Optional Sentence Transformers semantic embeddings
- Structured JSON logging
- Request correlation via `X-Request-ID`
- Dependency-aware readiness reporting
- Static typing and linting
- Unit tests and retrieval/embedding tests
- Docker-based local environment
- GitHub Actions CI
- Architecture Decision Records and research notes

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

For the lightweight local baseline, keep:

```env
MEMORY_BACKEND=in_memory
RETRIEVAL_BACKEND=hybrid
```

For model-backed semantic retrieval:

```bash
pip install .[semantic]
```

and set:

```env
RETRIEVAL_BACKEND=semantic
SEMANTIC_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

For PostgreSQL-backed operation, set `MEMORY_BACKEND=postgres` and run migrations:

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
  repositories/    persistence and embedding ports
  services/        application use cases and retrieval
  infrastructure/  database, cache, and embedding adapters
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
- [x] Request correlation and readiness checks
- [x] Embedding provider abstraction
- [x] Explainable hybrid retrieval baseline
- [x] Deterministic local embedding provider
- [x] Optional Sentence Transformers provider
- [ ] Persistent vector storage / pgvector adapter
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
