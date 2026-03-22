# Chunking Ablation Results

- Generated at: 2026-03-22T14:22:21.873852+00:00
- Questions file: `evaluation\questions.json`
- Cache enabled during eval: `False`
- Similarity threshold: `0.92`

## Summary Table

| Strategy | Samples | Successful | Errors | Avg Retrieved Contexts | Answer Relevancy | Faithfulness | Context Precision | Context Recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| recursive | 60 | 60 | 0 | 2.2667 | 0.5289 | 0.6828 | 0.3146 | 0.1453 |
| hierarchical | 60 | 60 | 0 | 2.2000 | 0.5714 | 0.7987 | 0.5285 | 0.2851 |

## Interpretation

- Use this table to compare the baseline `recursive` chunking against the advanced `hierarchical` parent-child strategy on the same question set.
- `Avg Retrieved Contexts` helps explain whether one strategy is returning broader or narrower evidence sets.
- For this project, `hierarchical` is the intended default when it improves retrieval coverage without hurting faithfulness.
