# Claude Certification Knowledge Assistant - Agentic RAG

A domain-specific **Agentic Retrieval-Augmented Generation (RAG)** system built to answer questions about the **Claude Certified Architect - Foundations** certification, Anthropic learning materials, and current course availability.

This project was developed for **RAG Assignment 3** and combines:

- **Adaptive RAG** for route selection
- **Corrective RAG** for retrieval repair and fallback
- **Self-RAG** for grounding and answer-quality checks
- **Hierarchical parent-child chunking** for local retrieval
- **Semantic caching** for repeated stable questions
- A **3-tier execution model** for direct, single-route, and multi-hop answers

---

## Table of Contents

- [Architecture Diagram](#architecture-diagram)
- [UI Preview](#ui-preview)
- [Project Overview](#project-overview)
- [Why This Is Agentic RAG](#why-this-is-agentic-rag)
- [Framework Choice and Why](#framework-choice-and-why)
- [Chunking Strategy and Why](#chunking-strategy-and-why)
- [Retrieval Strategy](#retrieval-strategy)
- [Semantic Cache](#semantic-cache)
- [System Design](#system-design)
- [Design Trade-offs](#design-trade-offs)
- [Evaluation](#evaluation)
- [Chunking Ablation](#chunking-ablation)
- [Repository Structure](#repository-structure)
- [Setup](#setup)
- [Running the Project](#running-the-project)

---

## Architecture Diagram

The detailed architecture diagram of the entire system 

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

#### Adaptive RAG Runtime Architecture
![Architecture Diagram](docs/architecture_diagram.png)

## UI Preview

### Multi-hop Run Example

#### Final response to the user

![Tier 2 Multi-hop RAG Response](docs/screenshots/TC3_UI_Tier%202%20Multi-hop%20RAG_response.JPG)

#### Execution trace

![Tier 2 Multi-hop RAG Execution Trace](docs/screenshots/TC3_UI_Execution%20Trace_Tier%202%20Multi-hop%20RAG.JPG)

Detailed UI screenshots and supporting submission artifacts are stored in:

- `docs/screenshots/` for UI, CLI, and notebook screenshots
- `docs/outputs/` for captured CLI text output and notebook export output

Reviewers can use the featured Tier 2 example above and refer to `docs/screenshots/` for the remaining UI test case screenshots.

## Project Overview

This system is designed to answer three kinds of questions:

| Tier | Description | Example |
| --- | --- | --- |
| Tier 0 | Direct LLM answer, no retrieval needed | "What is query decomposition?" |
| Tier 1 | Single-route retrieval from either local corpus or web | "According to the exam guide, what passing score is required?" |
| Tier 2 | Multi-hop retrieval that combines multiple sources or sub-questions | "Using the exam guide and current course listings, which course best aligns with MCP preparation?" |

## Why This Is Agentic RAG

This is not a simple retrieve-then-generate pipeline. The system makes decisions during execution:

- Should the question be answered directly or with retrieval?
- Should retrieval use the local corpus or web search?
- If retrieval is weak, should the query be rewritten?
- If local retrieval fails, should the system fall back to web search?
- If the answer is weak or unsupported, should the system retry?
- If the question contains multiple distinct intents, should it decompose and merge answers?

That decision-making behavior is what makes this an agentic RAG system.

## Framework Choice and Why

This project uses LangGraph as the main orchestration framework.

### Why LangGraph?

| Reason | Why it matters here |
| --- | --- |
| Branching control flow | The system routes queries across `llm_direct`, `vectorstore`, and `web_search` |
| Retry loops | Retrieval and generation both use bounded retry logic |
| Corrective retrieval | Weak retrieval can trigger rewrite and fallback |
| Self-RAG checks | Generated answers are graded before return |
| Multi-hop orchestration | Decomposed sub-questions can run independently and then merge |

A simpler chain-based framework would make this harder to maintain because routing, retries, and fallback logic would be buried in prompts instead of explicit execution flow.

### Core Libraries

| Library | Purpose |
| --- | --- |
| `langgraph` / `langchain` | Graph orchestration and node composition |
| `chromadb` / `langchain-chroma` | Local vector retrieval |
| `langchain-openai` | LLM and embedding integration |
| Brave Search integration | Web search for current information and fallback |
| `ragas` | Evaluation |
| `pydantic` | Structured planner outputs and validation |

## Chunking Strategy and Why

The default chunking strategy is hierarchical parent-child chunking.

### How it works

| Step | Description |
| --- | --- |
| 1. Split source docs | Documents are split into structured sections |
| 2. Create parent chunks | Larger parent chunks preserve broader context |
| 3. Create child chunks | Smaller child chunks improve retrieval precision |
| 4. Index child chunks | Child chunks are embedded and stored in Chroma |
| 5. Rehydrate parent context | Retrieved child chunks map back to larger parent sections via `parent_store.json` |

### Why this strategy?

| Benefit | Why it matters |
| --- | --- |
| Higher precision | Small child chunks improve semantic matching |
| Better answer grounding | Parent chunks preserve enough context for generation |
| Works well across mixed corpus sizes | Useful for both short markdown snapshots and the longer exam guide PDF |

### Trade-off

Flat chunking is simpler, but it often returns chunks that are either too small to answer confidently or too broad to retrieve precisely. Parent-child chunking adds implementation complexity, but it gives a better precision-context balance for this corpus.

> The chunking ablation shows that hierarchical parent-child chunking is the better default for this project. Although recursive chunking achieved slightly higher context recall, hierarchical chunking substantially improved faithfulness and context precision, while also slightly improving answer relevancy. Since this assistant is designed for certification and documentation QA, groundedness and precision were prioritized over retrieving a broader evidence set.

## Retrieval Strategy

The system supports two retrieval sources.

### Retrieval Sources

| Source | When used | Backing data / target |
| --- | --- | --- |
| Local corpus retrieval | Stable documentation, certification details, local course summaries | `data/raw/` |
| Web search (Brave Search) | Current listings, recent changes, fallback when local retrieval is weak | Anthropic public learning pages |

### Local Corpus Contents

| High-level document | File / source |
| --- | --- |
| Certification exam guide | `data/raw/Claude_Certified_Architect_Foundations_Certification_Exam_Guide.pdf` |
| Claude 101 snapshot | `data/raw/claude_101.md` |
| Building with the Claude API snapshot | `data/raw/Building with the Claude API.md` |
| Claude Code in Action snapshot | `data/raw/claude_code_in_action.md` |
| Introduction to Claude Cowork snapshot | `data/raw/Introduction to Claude Cowork.md` |
| Introduction to Model Context Protocol snapshot | `data/raw/introduction-to-model-context-protocol.md` |

### Web Targets

| High-level page | Purpose | URL |
| --- | --- | --- |
| Anthropic Learn | Top-level learning hub | `https://www.anthropic.com/learn` |
| Anthropic Courses catalog | Current course listings and public course pages | `https://anthropic.skilljar.com/` |

### Retrieval Policy

| Situation | Preferred route |
| --- | --- |
| Stable, source-specific knowledge | `vectorstore` |
| Current or recent information | `web_search` |
| Weak local retrieval | `rewrite -> retry -> web fallback` |
| General conceptual question | `llm_direct` |

## Semantic Cache

A semantic cache sits in front of the main pipeline.

| Feature | Current behavior |
| --- | --- |
| Cache type | Semantic similarity cache |
| Location | `src/cache/semantic_cache.py` |
| Default threshold | `0.92` cosine similarity |
| Scope | Tied to corpus version and chunking strategy |
| Bypass rule | Skips caching for time-sensitive questions |

### Why it was added

The cache reduces repeated work for stable questions and improves responsiveness, while still avoiding stale responses for current-information queries.

## System Design

### High-Level Flow

```text
User Question
    |
    v
Semantic Cache Check
    |
    +-- Cache hit -> return cached answer
    |
    +-- Cache miss
            |
            v
         Planner
            |
     +------+------+ 
     |             |
     v             v
  Single         Multi-hop
  Question       Decompose into
  Path           Sub-questions
     |             |
     v             v
   Router      Run single-question
     |         graph for each sub-question
     |             |
     +-- llm_direct
     +-- vectorstore
     +-- web_search
            |
            v
   Retrieval / Web Search
            |
            v
    Relevance Grading
            |
      +-----+-----+
      |           |
      v           v
   Good docs   Weak docs
      |           |
      |      Query Rewrite
      |           |
      |      Retry Retrieval
      |           |
      |      Web Fallback
      v
 Grounded Generation
      |
      v
Hallucination / Quality Check
      |
   +--+--+
   |     |
   v     v
Return  Retry
Answer  (bounded)
            |
            v
     Merge sub-answers
     (multi-hop only)
```

### Main Modules

| Module | Role |
| --- | --- |
| `src/api.py` | Top-level wrapper for cache, planning, routing, execution, and merge |
| `src/graph.py` | Core single-question graph orchestration |
| `src/nodes/planner.py` | Decides whether a query stays single or becomes multi-hop |
| `src/nodes/router.py` | Chooses `llm_direct`, `vectorstore`, or `web_search` |
| `src/nodes/retriever.py` | Retrieves local corpus chunks and rehydrates parent context |
| `src/nodes/rewriter.py` | Rewrites weak retrieval queries |
| `src/nodes/fallback.py` | Handles fallback search behavior |
| `src/nodes/generator.py` | Generates grounded answers |
| `src/nodes/grader.py` | Grades relevance, hallucination risk, and answer quality |
| `src/nodes/merge.py` | Merges decomposed sub-question answers |
| `src/cache/semantic_cache.py` | Semantic cache implementation |
| `src/ingestion/` | Document loading, chunking, and indexing |

## Design Trade-offs

| Decision | Why it was chosen | Trade-off |
| --- | --- | --- |
| LangGraph instead of a simple chain | Needed explicit routing, loops, and fallback | More code and orchestration complexity |
| Planner outside the single-question graph | Keeps `graph.py` focused on one question at a time | Top-level orchestration is split across files |
| Parent-child chunking | Better precision-context balance | More moving parts than flat chunking |
| Local corpus first, web second | Improves reproducibility during evaluation | Web answers may be fresher in some cases |
| Binary-style grading decisions | Easier debugging and stable control flow | Less nuanced than calibrated scoring |
| Bounded retries | Prevents runaway loops | Some edge cases may stop before the best answer is found |
| 3-tier routing | Makes planning and evaluation more interpretable | Tier 1 vs Tier 2 needs careful prompt and planner tuning |

## Evaluation

The evaluation dataset is stored in:

`evaluation/questions.json`

The main evaluation runner is:

```bash
python evaluation/run_ragas_eval.py
```

### Evaluation Outputs

| File | Purpose |
| --- | --- |
| `evaluation/results.json` | Raw per-sample metrics and tier observations |
| `evaluation/results.md` | Human-readable summary with findings |

### Metrics

These metrics were chosen to cover both answer quality and retrieval quality, since routed RAG failures can come from either the retrieval step or the answer generation step.

| Metric | Meaning |
| --- | --- |
| Answer Relevancy | How directly and completely the answer addresses the question |
| Faithfulness | Whether the answer is supported by the retrieved evidence |
| Context Precision | How much of the retrieved context is actually relevant |
| Context Recall | How much of the relevant evidence was successfully retrieved |

### Evaluation Design

The evaluation set is organized by routing tier:

| Tier | Purpose |
| --- | --- |
| Tier 0 | Direct-answer questions |
| Tier 1 | Single-source retrieval questions |
| Tier 2 | Multi-hop / multi-source questions |

This allows evaluation of both answer quality and routing behavior.

## Chunking Ablation

To compare recursive chunking against hierarchical parent-child chunking:

```bash
python evaluation/run_chunking_ablation.py
```

### Ablation Outputs

| File | Purpose |
| --- | --- |
| `evaluation/ablation_results.json` | Raw ablation results |
| `evaluation/ablation_results.md` | Human-readable ablation summary |

## Repository Structure

```text
RAG_Project_3/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- data/
|   |-- raw/
|   |-- chroma/
|   `-- cache/
|-- evaluation/
|   |-- questions.json
|   |-- run_ragas_eval.py
|   |-- run_chunking_ablation.py
|   |-- results.json
|   |-- results.md
|   |-- ablation_results.json
|   `-- ablation_results.md
|-- notebooks/
|   `-- demo.ipynb
|-- src/
|   |-- api.py
|   |-- graph.py
|   |-- model_config.py
|   |-- state.py
|   |-- tiering.py
|   |-- cache/
|   |-- ingestion/
|   `-- nodes/
`-- ui/
```

## Setup

### 1. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and configure the required keys:

```env
OPENAI_API_KEY=your_openai_key
BRAVE_SEARCH_API_KEY=your_brave_search_key
```

### 3. Build or rebuild the local index

```bash
python -m src.ingestion.ingestion_test
```

Rebuild the index whenever:

- the corpus changes
- chunking logic changes
- `data/chroma/` is stale

## Running the Project

### Single-question graph smoke test

```bash
python -m src.nodes.graph_test
```

### Adaptive wrapper test

```bash
python -m src.nodes.adaptive_test
```

### Semantic cache smoke test

```bash
python -m src.cache.semantic_cache_test
```

### RAGAS evaluation

```bash
python evaluation/run_ragas_eval.py
```

### Chunking ablation

```bash
python evaluation/run_chunking_ablation.py
```

### Demo notebook

`notebooks/demo.ipynb` demonstrates the `llm_direct`, `vectorstore`, `web_search`, and multi-hop branches. Open it in Jupyter or VS Code notebooks, run the cells in order, and review the returned outputs plus the final summary table for routes, reasons, and citations.

An exported static version of the notebook output is also included at `docs/outputs/demo_notebook_output.html` for review. If GitHub does not render the HTML preview directly, download it and open it locally in a browser.
