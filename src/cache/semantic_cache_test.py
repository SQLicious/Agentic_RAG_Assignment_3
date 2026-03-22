from src.api import run_adaptive_query

questions = [
    "What does the Claude certification exam guide cover?",
    "What topics are covered in the Claude Certified Architect Foundations Certification Exam Guide?",
    "What does the Claude certification exam guide cover?",  # exact repeat question which should hit cache
]

for q in questions:
    print("=" * 100)
    print("QUESTION:", q)

    result = run_adaptive_query(
        question=q,
        chunking_strategy="hierarchical",
        similarity_threshold=0.92,
    )

    print("TIER:", result.get("tier_label"))
    print("CACHE HIT:", result.get("cache_hit"))
    print("CACHE SIMILARITY:", result.get("cache_similarity"))
    print("CACHE SOURCE QUESTION:", result.get("cache_source_question"))
    print("PLAN TYPE:", result.get("plan_type"))
    print("FINAL ANSWER:", result.get("final_answer"))
    print("CITATIONS:", result.get("citations"))
