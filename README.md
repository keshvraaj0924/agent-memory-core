<div align="center">

# Agent Memory Core

### Memory infrastructure for intelligent agents

**Persistent • Explainable • Provider-Agnostic • Research-Driven**

[![CI](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml/badge.svg)](https://github.com/keshvraaj0924/agent-memory-core/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange)](#roadmap)

**Agent Memory Core** is an open-source, provider-agnostic memory layer for AI agents. It turns memory into an explicit systems problem—covering lifecycle, retrieval, ranking, persistence, observability, and evaluation through clean, testable engineering boundaries.

[Architecture](#architecture) · [Quick Start](#quick-start) · [API](#api) · [Research](#research) · [Roadmap](#roadmap)

</div>

---

## Why this exists

Modern AI agents can reason, call tools, and consume context. The harder systems problem is **remembering well**.

A useful memory system must answer questions such as:

- What information is worth storing?
- Which memory is relevant to the current task?
- How should recency and importance affect ranking?
- How do we avoid coupling the domain to one database or embedding provider?
- How do we measure whether better retrieval actually improves an agent?

Agent Memory Core is designed to make those questions **explicit, configurable, observable, and benchmarkable**.

## What makes it different

| Capability | What it provides |
|---|---|
| **Memory lifecycle** | Create, read, update, delete, access tracking |
| **Typed memory** | Working, episodic, semantic, preference, procedural |
| **Hybrid retrieval** | Lexical + semantic + recency + importance + type signals |
| **Explainable ranking** | Component-level scores for every retrieval result |
| **Provider boundaries** | Swap storage, cache, and embedding implementations |
| **Production foundations** | Async I/O, configuration, structured logs, health probes |
| **Engineering discipline** | Tests, typing, linting, Docker, CI, migrations |
| **Research workflow** | Explicit hypotheses, benchmark methodology, reproducible baselines |

---

## Architecture

```text
┌──────────────────────────────────────────────────────────────────────┐
│                         AI AGENT / APPLICATION                      │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         FastAPI / v1 API                            │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Memory Service                             │
│                                                                      │
│  Lifecycle  •  Retrieval  •  Ranking  •  Access Tracking  •  Policy │
└───────────────┬───────────────────────┬──────────────────────────────┘
                │                       │
                ▼                       ▼
┌────────────────────────┐   ┌─────────────────────────────────────────┐
│   Repository Ports     │   │            Retrieval Engine            │
│                        │   │                                         │
│  PostgreSQL            │   │  Lexical ─┐                             │
│  In-Memory             │   │  Semantic ├─► Multi-Factor Ranker       │
│  Future Vector Stores  │   │  Recency  │                             │
└───────────┬────────────┘   │  Importance│                            │
            │                │  Type      ┘                            │
            │                └──────────────────┬──────────────────────┘
            │                                   │
            ▼                                   ▼
┌────────────────────────┐         ┌──────────────────────────────────┐
│ PostgreSQL / pgvector  │         │     Embedding Provider Port      │
└────────────────────────┘         │  Deterministic • Transformers   │
                                   └──────────────────────────────────┘

                    ┌───────────────────────────────┐
                    │ Redis • Logs • Health • CI    │
                    └───────────────────────────────┘
```

### Core design principle

> **Domain policy should not know which database, cache, embedding model, or LLM vendor is underneath it.**

That separation is the foundation for both production flexibility and research iteration.

---

## Memory model

Agent Memory Core treats memory as more than a text blob.

```text
Working       → temporary task state
Episodic      → events and experiences
Semantic      → durable factual knowledge
Preference    → stable user preferences
Procedural    → reusable instructions / behaviors
```

Each memory also tracks:

```text
importance
created_at
updated_at
last_accessed_at
access_count
```

This makes memory behavior observable over time instead of treating retrieval as a black box.

---

## Retrieval model

The current baseline intentionally uses **explainable deterministic signals**.

```text
R(m, q) = α·lexical
        + β·semantic
        + γ·recency
        + δ·importance
        + ε·type_priority
```

### Default weights

```text
Lexical       0.35
Semantic      0.35
Recency       0.10
Importance    0.15
Type Match    0.05
```

Every result exposes the component scores, making ranking inspectable and suitable for controlled experiments.

### Embedding providers

```text
EmbeddingProvider
      │
      ├── HashEmbeddingProvider
      │     └── deterministic local baseline
      │
      └── SentenceTransformerEmbeddingProvider
            └── optional model-backed semantic embeddings
```

The lightweight local provider keeps development and tests deterministic. Model-backed embeddings can be enabled through the optional semantic dependency set.

---

## API

| Method | Endpoint | Description |
|:---:|---|---|
| `POST` | `/api/v1/memories` | Create a memory |
| `GET` | `/api/v1/memories/{id}` | Retrieve a memory |
| `PATCH` | `/api/v1/memories/{id}` | Update a memory |
| `DELETE` | `/api/v1/memories/{id}` | Delete a memory |
| `POST` | `/api/v1/memories/search` | Ranked hybrid retrieval |
| `GET` | `/api/v1/health` | Liveness probe |
| `GET` | `/api/v1/ready` | Dependency-aware readiness |

Search results include the overall rank plus the individual retrieval components, which is useful for debugging, evaluation, and future policy optimization.

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/keshvraaj0924/agent-memory-core.git
cd agent-memory-core
```

### 2. Configure

```bash
cp .env.example .env
```

For the lightweight development baseline:

```env
MEMORY_BACKEND=in_memory
RETRIEVAL_BACKEND=hybrid
```

### 3. Start with Docker

```bash
docker compose up --build
```

### 4. Verify the service

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
```

### 5. Open the API

- API: `http://localhost:8000`
- OpenAPI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Example

Create a preference memory:

```bash
curl -X POST http://localhost:8000/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "content": "User prefers Python 3.12 for AI projects.",
    "memory_type": "preference",
    "user_id": "user-123",
    "importance": 0.90
  }'
```

Search:

```bash
curl -X POST http://localhost:8000/api/v1/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "query": "Which Python version does the user prefer?",
    "limit": 5
  }'
```

The response contains:

```json
{
  "score": 0.87,
  "lexical_score": 0.75,
  "semantic_score": 0.91,
  "recency_score": 0.99,
  "importance_score": 0.90,
  "type_match_score": 1.0
}
```

> Example values above are illustrative; actual scores depend on the configured provider and stored memories.

---

## Production-oriented capabilities

- Async FastAPI application
- Pydantic v2 validation
- SQLAlchemy 2 + async PostgreSQL adapter
- Redis infrastructure boundary
- Configurable in-memory / PostgreSQL backends
- Embedding provider abstraction
- Hybrid explainable retrieval
- Alembic migrations
- Structured JSON logging
- Request correlation with `X-Request-ID`
- Liveness and dependency-aware readiness probes
- Static type checking with MyPy
- Linting and formatting with Ruff
- Pytest-based test suite
- Docker and Docker Compose
- GitHub Actions CI
- Security and contribution policies
- ADR-based architectural documentation
- Research and benchmark documentation

---

## Repository structure

```text
agent-memory-core/
│
├── app/
│   ├── api/                # HTTP transport + dependency injection
│   ├── core/               # config, logging, middleware, exceptions
│   ├── domain/             # memory entities + domain enums
│   ├── repositories/       # persistence / embedding ports
│   ├── services/           # application use cases + retrieval
│   ├── infrastructure/     # DB, cache, embedding adapters
│   └── schemas/             # API contracts
│
├── tests/                  # unit + regression tests
├── docs/
│   ├── architecture/      # system design
│   ├── decisions/          # architecture decision records
│   └── research/           # hypotheses + benchmarks
├── migrations/             # Alembic migrations
├── scripts/                # reproducible benchmark tooling
├── .github/workflows/      # CI automation
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── SECURITY.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

---

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run quality checks:

```bash
pytest
ruff check .
ruff format --check .
mypy app
```

Enable model-backed semantic retrieval:

```bash
pip install -e ".[semantic]"
```

Then configure:

```env
RETRIEVAL_BACKEND=semantic
SEMANTIC_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

For PostgreSQL-backed operation:

```bash
alembic upgrade head
```

---

## Research

Agent Memory Core is intentionally being developed as **both infrastructure and a research testbed**.

### Current hypothesis

> **A memory ranker that combines semantic relevance with recency, importance, and memory type can outperform semantic-only retrieval for agent-oriented memory workloads.**

### Planned evaluation

```text
Semantic-only
      vs
Hybrid retrieval
      ↓
Recall@K
MRR
NDCG@K
Latency
Score calibration
Context usefulness
```

The repository contains a benchmark methodology and deterministic regression runner so future retrieval changes can be measured rather than judged subjectively.

---

## Roadmap

### ✅ Foundation

- [x] Enterprise project structure
- [x] Versioned FastAPI API
- [x] Typed memory domain model
- [x] Repository abstraction
- [x] PostgreSQL persistence boundary
- [x] Redis boundary
- [x] Alembic migrations
- [x] Health/readiness endpoints
- [x] Structured observability

### ✅ Retrieval v0.3

- [x] Embedding provider abstraction
- [x] Deterministic local embedding baseline
- [x] Optional Sentence Transformers provider
- [x] Hybrid retrieval
- [x] Explainable score decomposition
- [x] Retrieval regression benchmark

### 🚧 Next

- [ ] Persistent vector storage / pgvector
- [ ] Memory deduplication
- [ ] Conflict-aware memory updates
- [ ] Memory consolidation
- [ ] Context-budget optimizer
- [ ] Agent-facing Python SDK
- [ ] Larger benchmark dataset
- [ ] Production deployment reference

### 🔬 Longer-term research

- [ ] Learned memory importance
- [ ] Adaptive retrieval weights
- [ ] Memory decay / forgetting policies
- [ ] Cross-session memory consolidation
- [ ] Cost-aware context selection
- [ ] Agent-level task benchmarks

---

## Engineering philosophy

> **Build the infrastructure first. Measure the intelligence second.**

The project favors:

- explicit contracts over hidden coupling
- replaceable providers over vendor lock-in
- measurable hypotheses over marketing claims
- deterministic baselines before learned systems
- small, reviewable architectural changes

---

## Contributing

Contributions, experiments, benchmark improvements, and architecture discussions are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development standards and workflow expectations.

## Security

For security issues, please follow the process in [SECURITY.md](SECURITY.md).

## License

Licensed under the **Apache License 2.0**. See [LICENSE](LICENSE).

<div align="center">

### Built to make agent memory measurable.

[⭐ Star the project](https://github.com/keshvraaj0924/agent-memory-core) · [Issues](https://github.com/keshvraaj0924/agent-memory-core/issues) · [Discussions](https://github.com/keshvraaj0924/agent-memory-core/discussions)

</div>
