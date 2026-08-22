# ADR-001: Explicit Domain and Infrastructure Boundaries

- **Status:** Accepted
- **Date:** 2026-08-22

## Context

Agent memory combines domain policy, persistence, retrieval, caching, and HTTP transport. Coupling these concerns makes it difficult to replace vendors, test memory behavior, or benchmark retrieval policies independently.

## Decision

Agent Memory Core uses explicit boundaries between:

1. **Domain** — memory entities and semantics.
2. **Application services** — use-case orchestration and policies.
3. **Repository ports** — interfaces for persistence and retrieval.
4. **Infrastructure** — concrete database, cache, and vector-store adapters.
5. **API** — transport schemas and HTTP concerns.

The domain layer must not import infrastructure implementations.

## Consequences

### Positive

- Persistence technologies can change without changing domain logic.
- Retrieval policies can be benchmarked independently.
- Unit tests can use deterministic adapters.
- API contracts remain independent from storage representation.

### Trade-offs

- More interfaces and files than a single-layer service.
- Dependency wiring must be explicit.

## Follow-up

PostgreSQL persistence, vector retrieval, and dependency injection will be added behind the repository boundaries established here.
