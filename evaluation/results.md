# Evaluation Results

- Generated at: 2026-03-22T05:22:32.601775+00:00
- Chunking strategy: `hierarchical`
- Cache enabled during eval: `False`
- Sample count: `60`

## Overall Metrics

| Metric | Mean |
| --- | ---: |
| Answer Relevancy | 0.5451 |
| Faithfulness | 0.7671 |
| Context Precision | 0.5374 |
| Context Recall | 0.3143 |

## Per-tier Metrics

| Tier | Samples | Answer Relevancy | Faithfulness | Context Precision | Context Recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| Tier 0 - llm_direct | 20 | 0.9326 | n/a | n/a | n/a |
| Tier 1 - single-route RAG | 33 | 0.3644 | 0.7960 | 0.4899 | 0.2799 |
| Tier 2 - multi-hop RAG | 7 | 0.2903 | 0.6311 | 0.7612 | 0.4762 |

## Counts by Tier

| Tier | Count |
| --- | ---: |
| Tier 0 - llm_direct | 20 |
| Tier 1 - single-route RAG | 33 |
| Tier 2 - multi-hop RAG | 7 |

## Counts by Plan Type

| Plan Type | Count |
| --- | ---: |
| single | 53 |
| multi | 7 |

## Observed vs Expected Tier

- Labeled samples: `60`
- Exact matches: `47`
- Mismatches: `13`

| ID | Expected Tier | Observed Tier |
| --- | --- | --- |
| tier2_local_exam_vs_claude101 | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_exam_vs_claude_code | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_exam_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_claude101_vs_claude_code | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_claude101_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_exam_and_claude101_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_exam_and_mcp_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_exam_and_claude_code_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_building_api_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_claude101_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_building_api_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_claude_code_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |
| tier2_local_mcp_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG |

## Per-sample Results

| ID | Expected Tier | Observed Tier | Plan | Final Route | Retrieved Contexts | Answer Relevancy | Faithfulness | Context Precision | Context Recall |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| tier0_prof_cert_definition | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_cert_vs_completion | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9626 | n/a | n/a | n/a |
| tier0_prompt_engineering | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_context_management | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_hallucination | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.6707 | n/a | n/a | n/a |
| tier0_semantic_cache | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.8992 | n/a | n/a | n/a |
| tier0_vectorstore | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.8442 | n/a | n/a | n/a |
| tier0_multihop | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9662 | n/a | n/a | n/a |
| tier0_singlehop_vs_multihop | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9417 | n/a | n/a | n/a |
| tier0_retrieval_precision | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.8606 | n/a | n/a | n/a |
| tier0_retrieval_recall | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_faithfulness | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9843 | n/a | n/a | n/a |
| tier0_answer_relevance | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9764 | n/a | n/a | n/a |
| tier0_chunking | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_parent_child_chunking | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9215 | n/a | n/a | n/a |
| tier0_router | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9561 | n/a | n/a | n/a |
| tier0_query_decomposition | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9013 | n/a | n/a | n/a |
| tier0_doc_snapshot | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 1.0000 | n/a | n/a | n/a |
| tier0_cache_bypass_recency | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.9812 | n/a | n/a | n/a |
| tier0_why_use_rag | Tier 0 - llm_direct | Tier 0 - llm_direct | single | llm_direct | 0 | 0.7862 | n/a | n/a | n/a |
| tier1_local_exam_scope | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 2 | 0.5246 | 1.0000 | 1.0000 | 0.5000 |
| tier1_local_exam_format_score | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 2 | 0.6740 | 1.0000 | 0.0000 | 0.5000 |
| tier1_local_exam_preparation | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 2 | 0.3074 | 1.0000 | 1.0000 | 0.5714 |
| tier1_local_exam_domains | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 2 | 0.5150 | 1.0000 | 0.0000 | 0.0000 |
| tier1_local_exam_scoring_scale | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 1 | 0.5623 | 1.0000 | 1.0000 | 1.0000 |
| tier1_local_exam_question_style | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 4 | 0.6888 | 1.0000 | 0.0000 | 0.0000 |
| tier1_local_claude101_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 2 | 0.8372 | 1.0000 | 0.0000 | 0.3333 |
| tier1_local_building_api_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 3 | 0.6842 | 1.0000 | 1.0000 | 1.0000 |
| tier1_local_claude_code_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 3 | 0.4481 | 0.7500 | 0.3333 | 0.0000 |
| tier1_local_mcp_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 3 | 0.6332 | 1.0000 | 1.0000 | 0.0000 |
| tier1_web_courses_list | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.7026 | 0.3333 | 0.0000 | 0.0000 |
| tier1_web_claude101_listed | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| tier1_web_building_api_listed | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.8838 | 1.0000 | 0.5000 | 0.0000 |
| tier1_web_claude_code_listed | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| tier1_web_mcp_listed | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.7905 | 1.0000 | 0.0000 | 0.0000 |
| tier1_web_claude101_page_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| tier1_web_building_api_page_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.7603 | 1.0000 | 0.5000 | 0.0000 |
| tier1_web_claude_code_page_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.5959 | 1.0000 | 0.0000 | 0.0000 |
| tier1_web_mcp_page_topics | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | vectorstore | 1 | 0.8327 | 0.7500 | 0.0000 | 0.0000 |
| tier1_web_builder_courses_count | Tier 1 - single-route RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.5000 | 0.3333 | 0.0000 | 0.0000 |
| tier2_local_exam_vs_claude101 | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 1 | 0.0000 | 0.5000 | 1.0000 | 0.5000 |
| tier2_local_exam_vs_building_api | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 5 | 0.0000 | 0.9375 | 1.0000 | 1.0000 |
| tier2_local_exam_vs_claude_code | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 1 | 0.0000 | 0.3333 | 1.0000 | 0.5000 |
| tier2_local_exam_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 2 | 0.0000 | 0.5000 | 1.0000 | 0.5000 |
| tier2_local_claude101_vs_claude_code | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 4 | 0.0000 | 0.6667 | 1.0000 | 0.5000 |
| tier2_local_claude101_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 0.6667 | 1.0000 | 0.0000 |
| tier2_local_exam_and_claude101_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 4 | 0.0000 | 0.5000 | 1.0000 | 0.6667 |
| tier2_local_exam_and_mcp_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | vectorstore | 2 | 0.5110 | 0.7500 | 1.0000 | 1.0000 |
| tier2_local_exam_and_claude_code_overlap | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 0.5000 | 1.0000 | 0.6667 |
| tier2_local_building_api_vs_mcp | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 0.0000 | 0.3333 | 0.0000 |
| tier2_local_claude101_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 0.7500 | 0.0000 | 0.0000 |
| tier2_local_building_api_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.5727 | 0.9333 | 0.5000 | 0.5000 |
| tier2_local_claude_code_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 1.0000 | 0.0000 | 0.0000 |
| tier2_local_mcp_plus_web_listing | Tier 2 - multi-hop RAG | Tier 1 - single-route RAG | single | web_search | 3 | 0.0000 | 1.0000 | 1.0000 | 0.5000 |
| tier2_exam_plus_web_mcp_alignment | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 6 | 0.4502 | 0.3636 | 0.6458 | 0.0000 |
| tier2_exam_plus_web_api_alignment | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 6 | 0.7980 | 0.1429 | 1.0000 | 0.3333 |
| tier2_exam_plus_web_claude_code_alignment | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 6 | 0.7841 | 0.6250 | 0.9167 | 0.3333 |
| tier2_exam_plus_web_builder_courses | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 8 | 0.0000 | 1.0000 | 0.3028 | 0.0000 |
| tier2_local_claude101_vs_web_claude101 | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 6 | 0.0000 | 0.6667 | 0.5250 | 0.6667 |
| tier2_local_claude_code_vs_web_claude_code | Tier 2 - multi-hop RAG | Tier 2 - multi-hop RAG | multi | multi_hop | 9 | 0.0000 | 0.6818 | 0.9379 | 1.0000 |

## Findings

- Faithfulness is relatively strong overall at 0.7671.
- Context recall is weaker overall at 0.3143.
- Observed-vs-expected tier mismatches: 13 out of 60 labeled samples.
- Over-decomposition and incomplete Tier 2 context aggregation were likely causes of weaker retrieval-side metrics in earlier runs.

## Sample Details

### tier0_prof_cert_definition
- Question: What is a professional certification?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A professional certification is a credential that validates job-relevant knowledge or skills against a defined standard, usually through an assessment rather than simple participation.
- Error: None

### tier0_cert_vs_completion
- Question: How is a professional certification different from a certificate of completion?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9626
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A professional certification verifies competence against an external standard, while a certificate of completion mainly shows that someone finished a course or learning activity.
- Error: None

### tier0_prompt_engineering
- Question: What is prompt engineering?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Prompt engineering is the practice of designing instructions and context so a language model produces more accurate, useful, and reliable outputs.
- Error: None

### tier0_context_management
- Question: What is context management in an AI system?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Context management is the practice of selecting, structuring, and maintaining the information given to a model so it can respond effectively without confusion or overload.
- Error: None

### tier0_hallucination
- Question: What is hallucination in a RAG system?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.6707
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Hallucination in a RAG system is when the model produces content that is unsupported, fabricated, or inconsistent with the retrieved evidence.
- Error: None

### tier0_semantic_cache
- Question: What is a semantic cache?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.8992
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A semantic cache stores answers for previously seen questions and reuses them for new questions that are meaningfully similar, rather than only exact string matches.
- Error: None

### tier0_vectorstore
- Question: What is a vector store in a RAG pipeline?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.8442
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A vector store is a database that stores embedding vectors so semantically similar documents or chunks can be retrieved for a query.
- Error: None

### tier0_multihop
- Question: What does multi-hop retrieval mean?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9662
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Multi-hop retrieval means answering a question by gathering and combining evidence from more than one retrieval step or source.
- Error: None

### tier0_singlehop_vs_multihop
- Question: How is single-hop retrieval different from multi-hop retrieval?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9417
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Single-hop retrieval uses one main retrieval step or evidence pool, while multi-hop retrieval combines evidence from multiple retrieval steps, sources, or sub-questions.
- Error: None

### tier0_retrieval_precision
- Question: What is retrieval precision?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.8606
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Retrieval precision is the proportion of retrieved items that are actually relevant to the question.
- Error: None

### tier0_retrieval_recall
- Question: What is retrieval recall?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Retrieval recall is the proportion of relevant information that the retriever successfully returns.
- Error: None

### tier0_faithfulness
- Question: What does faithfulness mean in RAG evaluation?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9843
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Faithfulness measures whether an answer is supported by the evidence provided to the model rather than invented or contradicted by the context.
- Error: None

### tier0_answer_relevance
- Question: What is answer relevance in an evaluation metric?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9764
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Answer relevance measures how directly and completely the answer addresses the user’s question.
- Error: None

### tier0_chunking
- Question: What is chunking in document retrieval?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Chunking is the process of splitting documents into smaller pieces so they can be indexed and retrieved more effectively.
- Error: None

### tier0_parent_child_chunking
- Question: What is parent-child chunking?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9215
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Parent-child chunking stores smaller child chunks for retrieval while preserving links to larger parent sections so broader context can be recovered during answering.
- Error: None

### tier0_router
- Question: What is a router in an adaptive RAG system?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9561
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A router is a component that decides which answering path to use, such as direct LLM response, vector store retrieval, web search, or multi-hop processing.
- Error: None

### tier0_query_decomposition
- Question: What is query decomposition?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9013
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Query decomposition is the process of breaking a complex question into smaller standalone sub-questions that can be answered and then merged.
- Error: None

### tier0_doc_snapshot
- Question: What is a local documentation snapshot?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 1.0000
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: A local documentation snapshot is a saved copy of source material stored locally so it can be indexed and queried without depending on live web access.
- Error: None

### tier0_cache_bypass_recency
- Question: Why should time-sensitive questions often bypass a semantic cache?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.9812
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Time-sensitive questions can become outdated quickly, so bypassing the semantic cache reduces the risk of returning stale answers.
- Error: None

### tier0_why_use_rag
- Question: Why use retrieval-augmented generation instead of relying only on a language model?
- Expected tier: Tier 0 - llm_direct
- Observed tier: Tier 0 - llm_direct
- Plan type: single
- Initial route: llm_direct
- Final route: llm_direct
- Retrieved contexts: 0
- Answer Relevancy: 0.7862
- Faithfulness: n/a
- Context Precision: n/a
- Context Recall: n/a
- Reference: Retrieval-augmented generation helps ground answers in external evidence, improves factual accuracy on source-specific questions, and reduces unsupported responses.
- Error: None

### tier1_local_exam_scope
- Question: According to the local certification exam guide PDF, what does the Claude Certified Architect – Foundations exam cover?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 2
- Answer Relevancy: 0.5246
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: The exam guide describes the exam content, domains, task statements, sample questions, and preparation strategies. It says the certification tests foundational knowledge across Claude Code, the Claude Agent SDK, the Claude API, and Model Context Protocol.
- Error: None

### tier1_local_exam_format_score
- Question: According to the local certification exam guide PDF, what response format and passing score does the exam use?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 2
- Answer Relevancy: 0.6740
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.5000
- Reference: The guide says all exam questions are multiple choice with one correct answer and three distractors. Results are reported on a scaled score from 100 to 1000, and the minimum passing score is 720.
- Error: None

### tier1_local_exam_preparation
- Question: According to the local certification exam guide PDF, how does the guide recommend preparing for the certification?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 2
- Answer Relevancy: 0.3074
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 0.5714
- Reference: The guide recommends building an agent with the Claude Agent SDK, configuring Claude Code for a real project, designing and testing MCP tools, building a structured data extraction pipeline, practicing prompt engineering and context management, reviewing escalation patterns, and completing the practice exam.
- Error: None

### tier1_local_exam_domains
- Question: According to the local certification exam guide PDF, which major knowledge areas are assessed?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 2
- Answer Relevancy: 0.5150
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: The exam guide assesses foundational knowledge across Claude Code, the Claude Agent SDK, the Claude API, and Model Context Protocol, along with practical understanding of workflows and system design patterns.
- Error: None

### tier1_local_exam_scoring_scale
- Question: According to the local certification exam guide PDF, what scoring scale is used for results?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 1
- Answer Relevancy: 0.5623
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 1.0000
- Reference: The exam guide states that results are reported on a scaled score from 100 to 1000.
- Error: None

### tier1_local_exam_question_style
- Question: According to the local certification exam guide PDF, how are the exam questions structured?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 4
- Answer Relevancy: 0.6888
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: The exam guide says the exam uses multiple-choice questions with one correct answer and three distractors.
- Error: None

### tier1_local_claude101_topics
- Question: According to the local claude_101.md snapshot, what topics does Claude 101 cover?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 2
- Answer Relevancy: 0.8372
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.3333
- Reference: Claude 101 covers core Claude usage for everyday work, including first conversations with Claude, getting better results, projects, artifacts, skills, connecting tools, enterprise search, research mode, role-based use cases, and it ends with a certificate of completion.
- Error: None

### tier1_local_building_api_topics
- Question: According to the local Building with the Claude API.md snapshot, what topics does that course cover?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 3
- Answer Relevancy: 0.6842
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 1.0000
- Reference: Building with the Claude API covers how developers use the Claude API to build applications, including prompting patterns, structured outputs, workflows, and practical implementation considerations.
- Error: None

### tier1_local_claude_code_topics
- Question: According to the local claude_code_in_action.md snapshot, what topics does Claude Code in Action cover?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 3
- Answer Relevancy: 0.4481
- Faithfulness: 0.7500
- Context Precision: 0.3333
- Context Recall: 0.0000
- Reference: Claude Code in Action covers coding assistant architecture, tool use, context management, automation, MCP servers, GitHub integration, and planning or reasoning workflows.
- Error: None

### tier1_local_mcp_topics
- Question: According to the local introduction-to-model-context-protocol.md snapshot, what topics does the course cover?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 3
- Answer Relevancy: 0.6332
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 0.0000
- Reference: Introduction to Model Context Protocol explains the purpose of MCP, how tools and context are exposed to models, and how MCP supports structured integrations between models and external systems.
- Error: None

### tier1_web_courses_list
- Question: As of today, which Claude-builder-relevant courses are currently listed on the Anthropic Courses site?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.7026
- Faithfulness: 0.3333
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, the Anthropic Courses site lists Claude Code in Action, Claude 101, Building with the Claude API, and Introduction to Model Context Protocol, along with additional AI Fluency courses.
- Error: None

### tier1_web_claude101_listed
- Question: As of today, is Claude 101 currently listed on the Anthropic Courses site?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: Yes. As of March 21, 2026, Claude 101 is listed on the Anthropic Courses site.
- Error: None

### tier1_web_building_api_listed
- Question: As of today, is Building with the Claude API currently listed on the Anthropic Courses site?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.8838
- Faithfulness: 1.0000
- Context Precision: 0.5000
- Context Recall: 0.0000
- Reference: Yes. As of March 21, 2026, Building with the Claude API is listed on the Anthropic Courses site.
- Error: None

### tier1_web_claude_code_listed
- Question: As of today, is Claude Code in Action currently listed on the Anthropic Courses site?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: Yes. As of March 21, 2026, Claude Code in Action is listed on the Anthropic Courses site.
- Error: None

### tier1_web_mcp_listed
- Question: As of today, is Introduction to Model Context Protocol currently listed on the Anthropic Courses site?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.7905
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: Yes. As of March 21, 2026, Introduction to Model Context Protocol is listed on the Anthropic Courses site.
- Error: None

### tier1_web_claude101_page_topics
- Question: As of today, what does the Anthropic Courses page say Claude 101 covers?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, the Anthropic Courses page describes Claude 101 as covering core Claude usage for everyday work, including features and workflows for practical use.
- Error: None

### tier1_web_building_api_page_topics
- Question: As of today, what does the Anthropic Courses page say Building with the Claude API covers?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.7603
- Faithfulness: 1.0000
- Context Precision: 0.5000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, the Anthropic Courses page describes Building with the Claude API as covering developer-oriented application-building patterns using the Claude API.
- Error: None

### tier1_web_claude_code_page_topics
- Question: As of today, what does the Anthropic Courses page say Claude Code in Action covers?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.5959
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, the Anthropic Courses page says Claude Code in Action covers coding assistant architecture, Claude Code tool use, context management, custom automation, MCP servers, GitHub integration, and planning or reasoning workflows.
- Error: None

### tier1_web_mcp_page_topics
- Question: As of today, what does the Anthropic Courses page say Introduction to Model Context Protocol covers?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 1
- Answer Relevancy: 0.8327
- Faithfulness: 0.7500
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, the Anthropic Courses page describes Introduction to Model Context Protocol as covering MCP concepts and structured integrations between models and external tools or systems.
- Error: None

### tier1_web_builder_courses_count
- Question: As of today, how many builder-relevant Claude courses are listed on the Anthropic Courses site among Claude 101, Claude Code in Action, Building with the Claude API, and Introduction to Model Context Protocol?
- Expected tier: Tier 1 - single-route RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.5000
- Faithfulness: 0.3333
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: As of March 21, 2026, all four of those builder-relevant courses are listed, so the count is four.
- Error: None

### tier2_local_exam_vs_claude101
- Question: Compare the local certification exam guide PDF and the local claude_101.md snapshot: how do they differ in focus?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 1
- Answer Relevancy: 0.0000
- Faithfulness: 0.5000
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: The exam guide focuses on assessed competencies, domains, and preparation for professional certification, while Claude 101 focuses on introductory and practical everyday use of Claude features and workflows.
- Error: None

### tier2_local_exam_vs_building_api
- Question: Compare the local certification exam guide PDF and the local Building with the Claude API.md snapshot: how do they differ in emphasis?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 5
- Answer Relevancy: 0.0000
- Faithfulness: 0.9375
- Context Precision: 1.0000
- Context Recall: 1.0000
- Reference: The exam guide emphasizes what knowledge and skills are assessed for certification, while Building with the Claude API emphasizes practical developer implementation patterns and API usage.
- Error: None

### tier2_local_exam_vs_claude_code
- Question: Compare the local certification exam guide PDF and the local claude_code_in_action.md snapshot: how do they differ in emphasis?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 1
- Answer Relevancy: 0.0000
- Faithfulness: 0.3333
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: The exam guide frames Claude Code as part of certification knowledge and preparation, while Claude Code in Action teaches hands-on coding assistant usage, tool use, automation, and engineering workflows.
- Error: None

### tier2_local_exam_vs_mcp
- Question: Compare the local certification exam guide PDF and the local introduction-to-model-context-protocol.md snapshot: how do they differ in emphasis?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 2
- Answer Relevancy: 0.0000
- Faithfulness: 0.5000
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: The exam guide treats Model Context Protocol as part of foundational certification knowledge, while the MCP course snapshot focuses on explaining the protocol and how structured integrations work.
- Error: None

### tier2_local_claude101_vs_claude_code
- Question: Compare the local claude_101.md snapshot and the local claude_code_in_action.md snapshot: how do the two courses differ in focus?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 4
- Answer Relevancy: 0.0000
- Faithfulness: 0.6667
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: Claude 101 is a broad introductory course about using Claude in everyday work, while Claude Code in Action focuses on coding workflows, tool use, automation, MCP servers, and engineering-oriented practices.
- Error: None

### tier2_local_claude101_vs_mcp
- Question: Compare the local claude_101.md snapshot and the local introduction-to-model-context-protocol.md snapshot: how do the two courses differ in scope?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 0.6667
- Context Precision: 1.0000
- Context Recall: 0.0000
- Reference: Claude 101 covers general Claude usage across common features and workflows, while Introduction to Model Context Protocol focuses specifically on MCP concepts, tool exposure, and structured model integrations.
- Error: None

### tier2_local_exam_and_claude101_overlap
- Question: Using the local certification exam guide PDF and the local claude_101.md snapshot, what themes appear in both sources?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 4
- Answer Relevancy: 0.0000
- Faithfulness: 0.5000
- Context Precision: 1.0000
- Context Recall: 0.6667
- Reference: Both sources cover Claude-related capabilities and practical usage concepts, but the exam guide frames them as assessed competencies while Claude 101 presents them as learning content for users.
- Error: None

### tier2_local_exam_and_mcp_overlap
- Question: Using the local certification exam guide PDF and the local introduction-to-model-context-protocol.md snapshot, what shared theme appears in both sources?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: vectorstore
- Retrieved contexts: 2
- Answer Relevancy: 0.5110
- Faithfulness: 0.7500
- Context Precision: 1.0000
- Context Recall: 1.0000
- Reference: Both include Model Context Protocol as an important topic, but the exam guide treats it as part of certification scope while the MCP course snapshot focuses on explanation and integration details.
- Error: None

### tier2_local_exam_and_claude_code_overlap
- Question: Using the local certification exam guide PDF and the local claude_code_in_action.md snapshot, what shared theme appears in both sources?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 0.5000
- Context Precision: 1.0000
- Context Recall: 0.6667
- Reference: Both involve Claude Code-related concepts and practical workflows, but the exam guide presents them as certification-relevant knowledge while Claude Code in Action focuses on hands-on engineering use.
- Error: None

### tier2_local_building_api_vs_mcp
- Question: Compare the local Building with the Claude API.md snapshot and the local introduction-to-model-context-protocol.md snapshot: how do they differ?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 0.0000
- Context Precision: 0.3333
- Context Recall: 0.0000
- Reference: Building with the Claude API focuses on application-building patterns using the Claude API, while Introduction to Model Context Protocol focuses on exposing tools and context through MCP for structured integrations.
- Error: None

### tier2_local_claude101_plus_web_listing
- Question: Using the local claude_101.md snapshot and the current Anthropic Courses site, what topics does Claude 101 cover locally, and is it currently listed?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 0.7500
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: The local Claude 101 snapshot says the course covers everyday Claude usage, including conversations, projects, artifacts, skills, tools, enterprise search, research mode, and role-based use cases. As of March 21, 2026, it is currently listed on the Anthropic Courses site.
- Error: None

### tier2_local_building_api_plus_web_listing
- Question: Using the local Building with the Claude API.md snapshot and the current Anthropic Courses site, what topics does that course cover locally, and is it currently listed?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.5727
- Faithfulness: 0.9333
- Context Precision: 0.5000
- Context Recall: 0.5000
- Reference: The local Building with the Claude API snapshot says the course covers developer use of the Claude API, including prompting patterns, structured outputs, workflows, and implementation considerations. As of March 21, 2026, it is currently listed on the Anthropic Courses site.
- Error: None

### tier2_local_claude_code_plus_web_listing
- Question: Using the local claude_code_in_action.md snapshot and the current Anthropic Courses site, what topics does Claude Code in Action cover locally, and is it currently listed?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: web_search
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 0.0000
- Context Recall: 0.0000
- Reference: The local Claude Code in Action snapshot says the course covers coding assistant architecture, tool use, context management, automation, MCP servers, GitHub integration, and planning or reasoning workflows. As of March 21, 2026, it is currently listed on the Anthropic Courses site.
- Error: None

### tier2_local_mcp_plus_web_listing
- Question: Using the local introduction-to-model-context-protocol.md snapshot and the current Anthropic Courses site, what topics does that course cover locally, and is it currently listed?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 1 - single-route RAG
- Plan type: single
- Initial route: vectorstore
- Final route: web_search
- Retrieved contexts: 3
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 1.0000
- Context Recall: 0.5000
- Reference: The local Introduction to Model Context Protocol snapshot says the course covers MCP concepts, tool and context exposure, and structured integrations between models and external systems. As of March 21, 2026, it is currently listed on the Anthropic Courses site.
- Error: None

### tier2_exam_plus_web_mcp_alignment
- Question: Using the local certification exam guide PDF and the current Anthropic Courses site, which currently listed course is most directly aligned with MCP preparation?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 6
- Answer Relevancy: 0.4502
- Faithfulness: 0.3636
- Context Precision: 0.6458
- Context Recall: 0.0000
- Reference: The exam guide includes MCP as a tested knowledge area, and as of March 21, 2026, Introduction to Model Context Protocol is currently listed on the Anthropic Courses site, making it the most directly aligned listed course for MCP preparation.
- Error: None

### tier2_exam_plus_web_api_alignment
- Question: Using the local certification exam guide PDF and the current Anthropic Courses site, which currently listed course is most directly aligned with Claude API preparation?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 6
- Answer Relevancy: 0.7980
- Faithfulness: 0.1429
- Context Precision: 1.0000
- Context Recall: 0.3333
- Reference: The exam guide includes the Claude API as a tested knowledge area, and as of March 21, 2026, Building with the Claude API is currently listed on the Anthropic Courses site, making it the most directly aligned listed course for API preparation.
- Error: None

### tier2_exam_plus_web_claude_code_alignment
- Question: Using the local certification exam guide PDF and the current Anthropic Courses site, which currently listed course is most directly aligned with Claude Code preparation?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 6
- Answer Relevancy: 0.7841
- Faithfulness: 0.6250
- Context Precision: 0.9167
- Context Recall: 0.3333
- Reference: The exam guide includes Claude Code within its scope, and as of March 21, 2026, Claude Code in Action is currently listed on the Anthropic Courses site, making it the most directly aligned listed course for Claude Code preparation.
- Error: None

### tier2_exam_plus_web_builder_courses
- Question: Using the local certification exam guide PDF and the current Anthropic Courses site, which currently listed courses align most clearly with the major builder knowledge areas named in the guide?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 8
- Answer Relevancy: 0.0000
- Faithfulness: 1.0000
- Context Precision: 0.3028
- Context Recall: 0.0000
- Reference: The exam guide names Claude Code, the Claude API, and MCP among its major knowledge areas. As of March 21, 2026, the currently listed courses that align most clearly are Claude Code in Action, Building with the Claude API, and Introduction to Model Context Protocol.
- Error: None

### tier2_local_claude101_vs_web_claude101
- Question: Using the local claude_101.md snapshot and the current Anthropic Courses page for Claude 101, how does the local summary align with the current course listing?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 6
- Answer Relevancy: 0.0000
- Faithfulness: 0.6667
- Context Precision: 0.5250
- Context Recall: 0.6667
- Reference: Both describe Claude 101 as a broad course about practical Claude usage. The local snapshot provides a fuller topic list including conversations, projects, artifacts, tools, enterprise search, research mode, and role-based use cases, while the current course page confirms the course is live and presents its current public description.
- Error: None

### tier2_local_claude_code_vs_web_claude_code
- Question: Using the local claude_code_in_action.md snapshot and the current Anthropic Courses page for Claude Code in Action, how does the local summary align with the current course listing?
- Expected tier: Tier 2 - multi-hop RAG
- Observed tier: Tier 2 - multi-hop RAG
- Plan type: multi
- Initial route: multi_hop
- Final route: multi_hop
- Retrieved contexts: 9
- Answer Relevancy: 0.0000
- Faithfulness: 0.6818
- Context Precision: 0.9379
- Context Recall: 1.0000
- Reference: Both describe Claude Code in Action as focused on coding assistant workflows and engineering usage. The local snapshot lists tool use, context management, automation, MCP servers, GitHub integration, and planning workflows, while the current course page confirms the course is live and presents its current public description.
- Error: None

## Notes

- Tier 0 samples use direct LLM answers, so retrieval-based metrics may be recorded as `n/a` when no retrieved contexts exist.
- Tier 2 scoring uses the top-level aggregated retrieved contexts returned by `run_adaptive_query()` across all sub-questions.
- Cache is disabled by default during evaluation to avoid misleading reuse of stale answers.
- Time-sensitive questions bypass semantic cache during normal runtime as well.
