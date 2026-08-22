# System Overview

## Layers

### API

FastAPI endpoints are responsible for HTTP transport, validation, versioning, and response serialization.

### Application

Services orchestrate use cases. They depend on repository ports rather than concrete storage engines.

### Domain

Memory entities and semantic rules remain independent of frameworks and infrastructure.

### Infrastructure

Adapters provide PostgreSQL persistence, Redis integration, and future vector-store implementations.

## Runtime flow

```text
HTTP Request
   ↓
API Schema Validation
   ↓
Memory Service
   ↓
Repository Port
   ↓
Infrastructure Adapter
   ↓
Persistence / Vector Store
```

## Reliability boundaries

- Liveness does not depend on external services.
- Readiness is a separate operational contract and will gain dependency checks as persistence wiring is enabled.
- Configuration is environment-driven.
- Logs are structured for machine ingestion.
- Infrastructure implementations remain replaceable.
