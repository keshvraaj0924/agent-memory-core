# Using Agent Memory Core

This guide is the fastest path from a fresh clone to a working memory service.

## 1. Local development

```bash
git clone https://github.com/keshvraaj0924/agent-memory-core.git
cd agent-memory-core
cp .env.example .env
pip install -e ".[dev]"
uvicorn main:app --reload
```

The API starts on `http://localhost:8000`.

## 2. Docker development

```bash
docker compose up --build
```

The default development configuration uses the deterministic in-memory backend so the service can start without an external vector database.

## 3. Check service health

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/ready
```

Use `/health` for process liveness and `/ready` to verify that configured dependencies are available.

## 4. Store a memory

```bash
curl -X POST http://localhost:8000/api/v1/memories \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The customer prefers quarterly reporting.",
    "memory_type": "preference",
    "user_id": "customer-001",
    "importance": 0.85
  }'
```

The response contains the memory UUID and lifecycle metadata.

## 5. Retrieve a memory

```bash
curl http://localhost:8000/api/v1/memories/<MEMORY_ID>
```

Reading a memory updates its access metadata. This is intentional: retrieval behavior is part of the memory model.

## 6. Search memories

```bash
curl -X POST http://localhost:8000/api/v1/memories/search \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "customer-001",
    "query": "What does the customer prefer for reporting?",
    "limit": 5
  }'
```

The response includes the overall ranking score and its component scores. This makes retrieval explainable and easy to benchmark.

## 7. Enable model-backed semantic retrieval

Install the optional dependency set:

```bash
pip install -e ".[semantic]"
```

Configure `.env`:

```env
RETRIEVAL_BACKEND=semantic
SEMANTIC_EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```

The first semantic request may download model artifacts through the configured embedding provider.

## 8. Enable PostgreSQL persistence

Set:

```env
MEMORY_BACKEND=postgres
DATABASE_URL=postgresql+asyncpg://memory:memory@localhost:5432/agent_memory
```

Run migrations:

```bash
alembic upgrade head
```

For Docker Compose, PostgreSQL is already defined as a service.

## 9. Use the service from Python

The HTTP API is the stable integration boundary. A typical application flow is:

```text
Agent task
   ↓
create memory candidates
   ↓
POST /memories
   ↓
POST /memories/search
   ↓
ranked memory context
   ↓
LLM / agent reasoning
```

The domain and repository boundaries are intentionally internal implementation details so storage and embedding providers can evolve without changing the API contract.

## 10. Run the engineering checks

```bash
pytest
ruff check .
ruff format --check .
mypy app
```

Run the retrieval regression benchmark:

```bash
python scripts/benchmark_retrieval.py
```

## Recommended integration pattern

Do not call the database or embedding implementation directly from an agent application. Use the API or the application service boundary. This keeps the agent integration independent from persistence details and allows the project to introduce vector stores, consolidation, and learned retrieval policies without forcing client changes.
