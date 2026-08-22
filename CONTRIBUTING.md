# Contributing

## Development workflow

1. Create a focused branch from `main`.
2. Make a small, reviewable change.
3. Add or update tests.
4. Run linting, formatting, type checks, and tests locally.
5. Open a pull request with context, scope, and validation notes.

## Quality bar

Changes should preserve domain boundaries, avoid unnecessary coupling, include tests for behavior changes, and document architectural decisions when introducing new system-level patterns.

## Commit style

Use concise Conventional Commit-style messages such as:

- `feat: add memory consolidation policy`
- `fix: handle stale memory retrieval`
- `test: cover ranking edge cases`
- `docs: add retrieval benchmark notes`

## Research changes

Experimental work should clearly separate hypotheses, implementation changes, datasets, metrics, and conclusions so results remain reproducible.
