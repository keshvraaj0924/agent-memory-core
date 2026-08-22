# Agent Memory Core

> Production-grade memory infrastructure for intelligent agents.

[![CI](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml/badge.svg)](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-production-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Agent Memory Core** is a provider-agnostic memory infrastructure service for AI agents. It provides explicit domain models, durable storage boundaries, retrieval abstractions, lifecycle management, and production observability so agent memory can be treated as a first-class system rather than prompt state.

## Why this project exists

Modern agents can call tools and reason over context, but durable memory introduces a separate systems problem: deciding what to store, how to represent it, when to retrieve it, how to rank conflicting memories, and how to stay inside a context budget.

This project turns those concerns into explicit, testable infrastructure.

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

The system is designed to support distinct memory semantics:

- **Working** — short-lived task state.
- **Episodic** — events and experiences.
- **Semantic** — durable factual knowledge.
- **Preference** — stable user preferences.
- **Procedural** — reusable instructions and behaviors.

## Retrieval research direction

The core research hypothesis is that memory retrieval should not rely on semantic similarity alone.

We will evaluate a ranking function of the form:

```text
R(m, q) = α·semantic + β·recency + γ·importance
        + δ·task_relevance + ε·type_priority
```

The repository will include reproducible benchmarks comparing semantic-only retrieval against multi-factor retrieval.

## Production goals

- FastAPI HTTP API with versioned endpoints
- Async application and infrastructure boundaries
- Pydantic v2 validation
- SQLAlchemy 2 persistence
- PostgreSQL-ready data layer
- Redis cache boundary
- Provider-agnostic vector repository interface
- Structured JSON logging
- Request IDs and health/readiness probes
- Static typing and linting
- Unit and integration testing
- Docker-based local environment
- GitHub Actions CI
- Architecture Decision Records (ADRs)

## Repository layout

```text
app/
  api/             HTTP transport and versioned endpoints
  core/            settings, logging, exceptions
  domain/          domain entities and enums
  repositories/    persistence ports
  services/        application use cases
  infrastructure/  database, cache, vector adapters
  schemas/         API contracts

tests/
  unit/
  integration/

docs/
  architecture/
  decisions/
  research/

.github/workflows/ CI and quality automation
```

## Quick start

```bash
cp .env.example .env
docker compose up --build
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

## Roadmap

- [x] Repository and architecture foundation
- [x] Application configuration and operational endpoints
- [x] Domain memory model
- [ ] PostgreSQL memory persistence
- [ ] Semantic/vector retrieval adapter
- [ ] Multi-factor retrieval scoring
- [ ] Memory consolidation and deduplication
- [ ] Agent-facing memory SDK
- [ ] Retrieval benchmark suite
- [ ] Production deployment reference

## Design philosophy

This project intentionally separates **domain policy** from **infrastructure implementation**. Storage providers, caches, embedding models, and LLM vendors should be replaceable without changing the memory domain.

The project is built incrementally so each stage remains reviewable, testable, and measurable.

## License

Apache-2.0
