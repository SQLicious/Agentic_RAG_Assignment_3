## Agentic RAG Architecture

```text
[INGESTION]              [ADAPTIVE RAG RUNTIME]                               [RAGAS EVALUATION]

Local Docs               User Query                                          questions.json
   ↓                     Semantic Cache                                          ├─ RAGAS Runner ─► results.json
Loader                      ↓                                                    │                    results.md
   ↓                     Cache Hit?                                              └─ Ablation Runner ─► ablation_results.json
Chunker                   ├─ yes → Cached Answer                                                      ablation_results.md
   ├─ Parent Store        └─ no
   ↓                           ↓
Embeddings                    Planner
   ↓                           ↓
ChromaDB                   Execution Tier?
                                ├─ Tier 0 → LLM Direct → Final Answer
                                ├─ Tier 1 → Route Selector
                                │              ├─ Retriever → Relevance → Relevant?
                                │              │                   ├─ yes → Generator → Hallucination → Quality → Final Answer
                                │              │                   └─ no → Rewriter → Retriever
                                │              │                                └─ fallback → Brave Search → Generator → Final Answer
                                │              └─ Brave Search → Generator
                                └─ Tier 2 → Decompose Query → Run Sub-graphs → Merge Answers → Final Answer with Citations to User
```


