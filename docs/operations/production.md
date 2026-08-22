# Production Operations Guide

This guide describes the minimum operational posture for deploying Agent Memory Core behind a production API gateway or load balancer.

## Runtime modes

Use these environment values for production:

```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
MEMORY_BACKEND=postgres
RETRIEVAL_BACKEND=hybrid
```

Use a managed PostgreSQL instance and Redis service in production. Do not use the in-memory backend for durable workloads.

## Required operational checks

### Liveness

```http
GET /api/v1/health
```

A successful liveness response means the process is running. It does not prove database or cache availability.

### Readiness

```http
GET /api/v1/ready
```

The endpoint returns `200` only when configured dependencies are healthy. A dependency failure returns `503 Service Unavailable`, allowing an orchestrator or load balancer to remove an unhealthy instance from service.

## Database migrations

Run migrations before enabling traffic after a schema change:

```bash
alembic upgrade head
```

Migrations are version-controlled under `migrations/versions/` and should be applied through the deployment pipeline rather than manually editing production tables.

## Observability

Application logs are emitted as structured JSON. Requests carry an `X-Request-ID` correlation identifier, which should be propagated into centralized logs and tracing infrastructure.

Recommended production signals:

- request rate
- error rate
- P50/P95/P99 latency
- readiness failures
- PostgreSQL pool saturation
- Redis availability
- retrieval latency
- retrieval result counts
- embedding latency
- memory creation/search rates

## Security baseline

- Store credentials in a secret manager, not `.env` files committed to source control.
- Restrict CORS origins to trusted frontends.
- Terminate TLS at the edge or service mesh.
- Apply network policy so PostgreSQL and Redis are not publicly reachable.
- Run the application as the non-root `appuser` configured by the Docker image.
- Keep dependency versions reviewed and updated through the normal maintenance process.

## Scaling model

The API layer is designed to be horizontally scalable because application services do not own durable state. Durable state belongs in PostgreSQL, while Redis is an optional shared infrastructure boundary.

```text
                    Load Balancer
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
           API-1       API-2       API-N
             │           │           │
             └───────────┼───────────┘
                         │
                 ┌───────┴────────┐
                 ▼                ▼
             PostgreSQL         Redis
```

## Release checklist

Before a production release:

```bash
make check
make benchmark
alembic upgrade head
```

Then verify:

1. `/api/v1/health` returns `200`.
2. `/api/v1/ready` returns `200`.
3. A memory can be created and retrieved.
4. Search returns explainable ranking components.
5. Logs contain request correlation identifiers.
6. No secrets are present in the built image or repository.
