from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

try:
    from evaluation.run_ragas_eval import DEFAULT_QUESTIONS_PATH, run_evaluation
except ModuleNotFoundError:
    from run_ragas_eval import DEFAULT_QUESTIONS_PATH, run_evaluation

DEFAULT_OUTPUT_JSON = Path("evaluation/ablation_results.json")
DEFAULT_OUTPUT_MD = Path("evaluation/ablation_results.md")


def _safe_mean(values: list[float]) -> float | None:
    if not values:
        return None
    return round(mean(values), 4)


def _format_metric(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _strategy_summary(payload: dict[str, Any]) -> dict[str, Any]:
    samples = payload["samples"]
    successful = [sample for sample in samples if not sample.get("error")]
    contextful = [
        sample.get("retrieved_context_count", 0)
        for sample in successful
        if sample.get("retrieved_context_count") is not None
    ]

    return {
        "chunking_strategy": payload["chunking_strategy"],
        "sample_count": len(samples),
        "successful_samples": len(successful),
        "error_count": len(samples) - len(successful),
        "avg_retrieved_contexts": _safe_mean(contextful),
        "answer_relevancy_mean": payload["summary"].get("answer_relevancy_mean"),
        "faithfulness_mean": payload["summary"].get("faithfulness_mean"),
        "context_precision_mean": payload["summary"].get("context_precision_mean"),
        "context_recall_mean": payload["summary"].get("context_recall_mean"),
    }


def _build_markdown(
    *,
    generated_at: str,
    questions_path: Path,
    cache_enabled: bool,
    similarity_threshold: float,
    comparisons: list[dict[str, Any]],
) -> str:
    lines = [
        "# Chunking Ablation Results",
        "",
        f"- Generated at: {generated_at}",
        f"- Questions file: `{questions_path}`",
        f"- Cache enabled during eval: `{cache_enabled}`",
        f"- Similarity threshold: `{similarity_threshold}`",
        "",
        "## Summary Table",
        "",
        "| Strategy | Samples | Successful | Errors | Avg Retrieved Contexts | Answer Relevancy | Faithfulness | Context Precision | Context Recall |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in comparisons:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["chunking_strategy"],
                    str(row["sample_count"]),
                    str(row["successful_samples"]),
                    str(row["error_count"]),
                    _format_metric(row["avg_retrieved_contexts"]),
                    _format_metric(row["answer_relevancy_mean"]),
                    _format_metric(row["faithfulness_mean"]),
                    _format_metric(row["context_precision_mean"]),
                    _format_metric(row["context_recall_mean"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Use this table to compare the baseline `recursive` chunking against the advanced `hierarchical` parent-child strategy on the same question set.",
            "- `Avg Retrieved Contexts` helps explain whether one strategy is returning broader or narrower evidence sets.",
            "- For this project, `hierarchical` is the intended default when it improves retrieval coverage without hurting faithfulness.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run recursive vs hierarchical chunking ablation.")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_PATH)
    parser.add_argument("--similarity-threshold", type=float, default=0.92)
    parser.add_argument("--use-cache", action="store_true", help="Allow semantic cache during ablation runs.")
    parser.add_argument(
        "--strategies",
        nargs="+",
        default=["recursive", "hierarchical"],
        help="Chunking strategies to compare.",
    )
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    payloads = [
        run_evaluation(
            questions_path=args.questions,
            chunking_strategy=strategy,
            similarity_threshold=args.similarity_threshold,
            use_cache=args.use_cache,
        )
        for strategy in args.strategies
    ]

    comparisons = [_strategy_summary(payload) for payload in payloads]
    generated_at = datetime.now(timezone.utc).isoformat()
    output = {
        "generated_at": generated_at,
        "questions_path": str(args.questions),
        "cache_enabled": args.use_cache,
        "similarity_threshold": args.similarity_threshold,
        "comparisons": comparisons,
        "runs": payloads,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        _build_markdown(
            generated_at=generated_at,
            questions_path=args.questions,
            cache_enabled=args.use_cache,
            similarity_threshold=args.similarity_threshold,
            comparisons=comparisons,
        ),
        encoding="utf-8",
    )

    print(f"Wrote ablation JSON to {args.output_json}")
    print(f"Wrote ablation Markdown to {args.output_md}")


if __name__ == "__main__":
    main()
