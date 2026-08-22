# Memory Retrieval Hypothesis

## Hypothesis

Pure semantic similarity is insufficient for agent memory retrieval because relevance also depends on recency, importance, task alignment, and memory type.

## Candidate scoring model

```text
score(m, q) = α·semantic_similarity
           + β·recency
           + γ·importance
           + δ·task_relevance
           + ε·type_priority
```

## Experimental plan

Compare retrieval policies under the same memory corpus and query set:

1. semantic similarity only
2. semantic + recency
3. semantic + importance
4. semantic + recency + importance
5. full multi-factor ranking

## Metrics

- Recall@K
- MRR
- NDCG@K
- context tokens consumed
- retrieval latency
- answer accuracy after memory injection

## Success criterion

The multi-factor policy should improve task-relevant retrieval quality without introducing unacceptable retrieval latency or context growth.
