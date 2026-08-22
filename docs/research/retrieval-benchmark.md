# Retrieval Benchmark Plan

## Research question

Does hybrid memory ranking outperform a similarity-only baseline when relevance depends on more than semantic proximity?

## Baselines

1. Lexical-only retrieval.
2. Semantic-only retrieval.
3. Hybrid retrieval with lexical + semantic + recency + importance + type priority.

## Metrics

- Recall@1
- Recall@5
- Mean Reciprocal Rank (MRR)
- NDCG@5
- Score calibration by relevance bucket
- P50/P95 retrieval latency
- Candidate count per query

## Evaluation protocol

Each benchmark sample contains a query, a user identifier, a set of candidate memories, and one or more relevant memory identifiers.

The evaluator must use fixed seeds and a committed dataset so results can be reproduced by CI or a researcher running the project locally.

## Planned experiment matrix

| Experiment | Lexical | Semantic | Recency | Importance | Type |
|---|---:|---:|---:|---:|---:|
| L0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| S0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| H1 | 0.35 | 0.35 | 0.10 | 0.15 | 0.05 |

## Important constraint

The deterministic hash embedding provider is a systems baseline for wiring and regression tests. It must not be presented as evidence of production semantic quality. Model-backed results will be reported separately using the configured Sentence Transformers provider.

## Expected outcome

The goal is not to assume hybrid retrieval wins. The goal is to measure when additional memory signals improve ranking and to identify the latency and quality trade-offs introduced by each signal.
