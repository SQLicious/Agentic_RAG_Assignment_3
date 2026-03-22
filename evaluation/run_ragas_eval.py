from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api import run_adaptive_query
from src.tiering import TIER_LABELS

DEFAULT_QUESTIONS_PATH = Path("evaluation/questions.json")
DEFAULT_RESULTS_JSON = Path("evaluation/results.json")
DEFAULT_RESULTS_MD = Path("evaluation/results.md")
TIER_ORDER = ["tier_0", "tier_1", "tier_2"]
PLAN_ORDER = ["single", "multi"]


def _load_questions(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe_mean(values: list[float | None]) -> float | None:
    numeric_values = [value for value in values if value is not None]
    if not numeric_values:
        return None
    return round(mean(numeric_values), 4)


def _format_metric(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _format_text(value: Any) -> str:
    if value is None:
        return "n/a"
    return str(value)


def _format_tier_label(value: Any) -> str:
    if value is None:
        return "n/a"
    return _format_text(TIER_LABELS.get(value, value))


def _extract_metric_row(df, metric_names: list[str]) -> list[dict[str, Any]]:
    rows = df.to_dict(orient="records")
    normalized_rows: list[dict[str, Any]] = []

    for row in rows:
        normalized = {"user_input": row.get("user_input")}
        for metric_name in metric_names:
            normalized[metric_name] = row.get(metric_name)
        normalized_rows.append(normalized)

    return normalized_rows


def _run_ragas(
    rows: list[dict[str, Any]],
    *,
    metric_kind: str,
) -> list[dict[str, Any]]:
    try:
        from ragas import EvaluationDataset, evaluate
        from ragas.metrics._answer_relevance import AnswerRelevancy
        from ragas.metrics._context_precision import ContextPrecision
        from ragas.metrics._context_recall import ContextRecall
        from ragas.metrics._faithfulness import Faithfulness
    except ImportError as exc:
        raise RuntimeError(
            "RAGAS is not installed. Install it with `uv pip install --python .venv/Scripts/python.exe ragas` "
            "or add it from requirements.txt before running evaluation."
        ) from exc

    from src.model_config import get_embeddings, get_grader_llm

    dataset = EvaluationDataset.from_list(rows)
    llm = get_grader_llm()
    embeddings = get_embeddings()

    if metric_kind == "answer":
        metric_names = ["answer_relevancy"]
        metrics = [AnswerRelevancy(strictness=1)]
    elif metric_kind == "rag":
        metric_names = ["faithfulness", "context_precision", "context_recall"]
        metrics = [Faithfulness(), ContextPrecision(), ContextRecall()]
    else:
        raise ValueError(f"Unsupported metric kind: {metric_kind}")

    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
    )

    if not hasattr(result, "to_pandas"):
        raise RuntimeError("Unexpected RAGAS result type: missing to_pandas()")

    return _extract_metric_row(result.to_pandas(), metric_names)


def _metric_summary(samples: list[dict[str, Any]]) -> dict[str, float | None]:
    return {
        "sample_count": len(samples),
        "answer_relevancy_mean": _safe_mean(
            [sample.get("answer_relevancy") for sample in samples]
        ),
        "faithfulness_mean": _safe_mean(
            [sample.get("faithfulness") for sample in samples]
        ),
        "context_precision_mean": _safe_mean(
            [sample.get("context_precision") for sample in samples]
        ),
        "context_recall_mean": _safe_mean(
            [sample.get("context_recall") for sample in samples]
        ),
    }


def _count_by(samples: list[dict[str, Any]], field: str, order: list[str] | None = None) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for sample in samples:
        value = sample.get(field) or "n/a"
        counts[str(value)] = counts.get(str(value), 0) + 1

    if order:
        ordered_keys = [key for key in order if key in counts]
        ordered_keys.extend(sorted(key for key in counts if key not in ordered_keys))
    else:
        ordered_keys = sorted(counts)

    return [{"name": key, "count": counts[key]} for key in ordered_keys]


def _per_tier_summary(samples: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []

    for tier in TIER_ORDER:
        tier_samples = [sample for sample in samples if sample.get("tier") == tier]
        rows.append(
            {
                "tier": tier,
                "tier_label": TIER_LABELS[tier],
                **_metric_summary(tier_samples),
            }
        )

    return rows


def _expected_vs_observed(samples: list[dict[str, Any]]) -> dict[str, Any]:
    with_expected = [sample for sample in samples if sample.get("expected_tier")]
    exact_matches = sum(
        1 for sample in with_expected if sample.get("tier") == sample.get("expected_tier")
    )
    mismatches = [
        {
            "id": sample["id"],
            "expected_tier": sample.get("expected_tier"),
            "observed_tier": sample.get("tier"),
        }
        for sample in with_expected
        if sample.get("tier") != sample.get("expected_tier")
    ]

    return {
        "evaluated_samples": len(with_expected),
        "exact_matches": exact_matches,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }


def _build_findings(summary: dict[str, Any]) -> list[str]:
    overall = summary["overall"]
    expected = summary["expected_vs_observed"]

    return [
        f"Faithfulness is relatively strong overall at {_format_metric(overall['faithfulness_mean'])}.",
        f"Context recall is weaker overall at {_format_metric(overall['context_recall_mean'])}.",
        f"Observed-vs-expected tier mismatches: {expected['mismatch_count']} out of {expected['evaluated_samples']} labeled samples.",
        "Over-decomposition and incomplete Tier 2 context aggregation were likely causes of weaker retrieval-side metrics in earlier runs.",
    ]


def _build_markdown(
    *,
    generated_at: str,
    chunking_strategy: str,
    cache_enabled: bool,
    summary: dict[str, Any],
    samples: list[dict[str, Any]],
) -> str:
    overall = summary["overall"]
    tier_rows = summary["per_tier"]
    tier_counts = summary["counts_by_tier"]
    plan_counts = summary["counts_by_plan_type"]
    expected = summary["expected_vs_observed"]
    findings = summary["findings"]

    lines = [
        "# Evaluation Results",
        "",
        f"- Generated at: {generated_at}",
        f"- Chunking strategy: `{chunking_strategy}`",
        f"- Cache enabled during eval: `{cache_enabled}`",
        f"- Sample count: `{overall['sample_count']}`",
        "",
        "## Overall Metrics",
        "",
        "| Metric | Mean |",
        "| --- | ---: |",
        f"| Answer Relevancy | {_format_metric(overall['answer_relevancy_mean'])} |",
        f"| Faithfulness | {_format_metric(overall['faithfulness_mean'])} |",
        f"| Context Precision | {_format_metric(overall['context_precision_mean'])} |",
        f"| Context Recall | {_format_metric(overall['context_recall_mean'])} |",
        "",
        "## Per-tier Metrics",
        "",
        "| Tier | Samples | Answer Relevancy | Faithfulness | Context Precision | Context Recall |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for row in tier_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["tier_label"],
                    str(row["sample_count"]),
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
            "## Counts by Tier",
            "",
            "| Tier | Count |",
            "| --- | ---: |",
        ]
    )

    for row in tier_counts:
        label = TIER_LABELS.get(row["name"], row["name"])
        lines.append(f"| {label} | {row['count']} |")

    lines.extend(
        [
            "",
            "## Counts by Plan Type",
            "",
            "| Plan Type | Count |",
            "| --- | ---: |",
        ]
    )

    for row in plan_counts:
        lines.append(f"| {row['name']} | {row['count']} |")

    lines.extend(
        [
            "",
            "## Observed vs Expected Tier",
            "",
            f"- Labeled samples: `{expected['evaluated_samples']}`",
            f"- Exact matches: `{expected['exact_matches']}`",
            f"- Mismatches: `{expected['mismatch_count']}`",
            "",
            "| ID | Expected Tier | Observed Tier |",
            "| --- | --- | --- |",
        ]
    )

    for mismatch in expected["mismatches"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    _format_text(mismatch["id"]),
                    _format_tier_label(mismatch["expected_tier"]),
                    _format_tier_label(mismatch["observed_tier"]),
                ]
            )
            + " |"
        )

    if not expected["mismatches"]:
        lines.append("| none | n/a | n/a |")

    lines.extend(
        [
            "",
            "## Per-sample Results",
            "",
            "| ID | Expected Tier | Observed Tier | Plan | Final Route | Retrieved Contexts | Answer Relevancy | Faithfulness | Context Precision | Context Recall |",
            "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for sample in samples:
        lines.append(
            "| "
            + " | ".join(
                [
                    sample["id"],
                    _format_tier_label(sample.get("expected_tier")),
                    _format_text(sample.get("tier_label") or _format_tier_label(sample.get("tier"))),
                    _format_text(sample.get("plan_type", "n/a")),
                    _format_text(sample.get("final_route", "n/a")),
                    str(sample.get("retrieved_context_count", 0)),
                    _format_metric(sample.get("answer_relevancy")),
                    _format_metric(sample.get("faithfulness")),
                    _format_metric(sample.get("context_precision")),
                    _format_metric(sample.get("context_recall")),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )

    for finding in findings:
        lines.append(f"- {finding}")

    lines.extend(
        [
            "",
            "## Sample Details",
            "",
        ]
    )

    for sample in samples:
        lines.extend(
            [
                f"### {sample['id']}",
                f"- Question: {sample['user_input']}",
                f"- Expected tier: {_format_tier_label(sample.get('expected_tier'))}",
                f"- Observed tier: {_format_text(sample.get('tier_label') or _format_tier_label(sample.get('tier')))}",
                f"- Plan type: {_format_text(sample.get('plan_type', 'n/a'))}",
                f"- Initial route: {_format_text(sample.get('initial_route', 'n/a'))}",
                f"- Final route: {_format_text(sample.get('final_route', 'n/a'))}",
                f"- Retrieved contexts: {sample.get('retrieved_context_count', 0)}",
                f"- Answer Relevancy: {_format_metric(sample.get('answer_relevancy'))}",
                f"- Faithfulness: {_format_metric(sample.get('faithfulness'))}",
                f"- Context Precision: {_format_metric(sample.get('context_precision'))}",
                f"- Context Recall: {_format_metric(sample.get('context_recall'))}",
                f"- Reference: {sample['reference']}",
                f"- Error: {sample.get('error', 'none')}",
                "",
            ]
        )

    lines.extend(
        [
            "## Notes",
            "",
            "- Tier 0 samples use direct LLM answers, so retrieval-based metrics may be recorded as `n/a` when no retrieved contexts exist.",
            "- Tier 2 scoring uses the top-level aggregated retrieved contexts returned by `run_adaptive_query()` across all sub-questions.",
            "- Cache is disabled by default during evaluation to avoid misleading reuse of stale answers.",
            "- Time-sensitive questions bypass semantic cache during normal runtime as well.",
            "",
        ]
    )

    return "\n".join(lines)


def run_evaluation(
    *,
    questions_path: Path = DEFAULT_QUESTIONS_PATH,
    chunking_strategy: str = "hierarchical",
    similarity_threshold: float = 0.92,
    use_cache: bool = False,
) -> dict[str, Any]:
    questions = _load_questions(questions_path)

    sample_results: list[dict[str, Any]] = []
    answer_rows: list[dict[str, Any]] = []
    rag_rows: list[dict[str, Any]] = []

    for case in questions:
        sample = {
            "id": case["id"],
            "user_input": case["question"],
            "reference": case["reference"],
            "expected_tier": case.get("tier"),
            "expected_route": case.get("expected_route"),
            "response": "",
            "tier": None,
            "tier_label": None,
            "plan_type": None,
            "cache_hit": False,
            "cache_allowed": False,
            "initial_route": None,
            "final_route": None,
            "retrieved_contexts": [],
            "retrieved_context_count": 0,
            "subquestion_count": 0,
            "error": None,
        }

        try:
            result = run_adaptive_query(
                question=case["question"],
                chunking_strategy=chunking_strategy,
                similarity_threshold=similarity_threshold,
                use_cache=use_cache,
            )
        except Exception as exc:
            sample["error"] = f"{type(exc).__name__}: {exc}"
            sample_results.append(sample)
            continue

        sample.update(
            {
                "response": result.get("final_answer", ""),
                "tier": result.get("tier"),
                "tier_label": result.get("tier_label"),
                "plan_type": result.get("plan_type"),
                "cache_hit": result.get("cache_hit"),
                "cache_allowed": result.get("cache_allowed"),
                "initial_route": result.get("initial_route"),
                "final_route": result.get("final_route"),
                "retrieved_contexts": result.get("retrieved_contexts", []),
                "retrieved_context_count": result.get("retrieved_context_count", 0),
                "subquestion_count": len(result.get("sub_results", [])),
            }
        )
        sample_results.append(sample)

        answer_rows.append(
            {
                "user_input": sample["user_input"],
                "response": sample["response"],
                "retrieved_contexts": sample["retrieved_contexts"],
                "reference": sample["reference"],
            }
        )

        if sample["retrieved_contexts"]:
            rag_rows.append(
                {
                    "user_input": sample["user_input"],
                    "response": sample["response"],
                    "retrieved_contexts": sample["retrieved_contexts"],
                    "reference": sample["reference"],
                }
            )

    answer_scores = (
        {
            row["user_input"]: row
            for row in _run_ragas(answer_rows, metric_kind="answer")
        }
        if answer_rows
        else {}
    )
    rag_scores = (
        {
            row["user_input"]: row
            for row in _run_ragas(rag_rows, metric_kind="rag")
        }
        if rag_rows
        else {}
    )

    for sample in sample_results:
        answer_row = answer_scores.get(sample["user_input"], {})
        rag_row = rag_scores.get(sample["user_input"], {})

        sample["answer_relevancy"] = answer_row.get("answer_relevancy")
        sample["faithfulness"] = rag_row.get("faithfulness")
        sample["context_precision"] = rag_row.get("context_precision")
        sample["context_recall"] = rag_row.get("context_recall")

    generated_at = datetime.now(timezone.utc).isoformat()
    overall = _metric_summary(sample_results)
    summary = {
        "overall": overall,
        "sample_count": overall["sample_count"],
        "answer_relevancy_mean": overall["answer_relevancy_mean"],
        "faithfulness_mean": overall["faithfulness_mean"],
        "context_precision_mean": overall["context_precision_mean"],
        "context_recall_mean": overall["context_recall_mean"],
        "per_tier": _per_tier_summary(sample_results),
        "counts_by_tier": _count_by(sample_results, "tier", order=TIER_ORDER),
        "counts_by_plan_type": _count_by(sample_results, "plan_type", order=PLAN_ORDER),
        "expected_vs_observed": _expected_vs_observed(sample_results),
    }
    summary["findings"] = _build_findings(summary)

    return {
        "generated_at": generated_at,
        "chunking_strategy": chunking_strategy,
        "cache_enabled": use_cache,
        "summary": summary,
        "samples": sample_results,
    }


def write_evaluation_outputs(
    payload: dict[str, Any],
    *,
    output_json: Path = DEFAULT_RESULTS_JSON,
    output_md: Path = DEFAULT_RESULTS_MD,
) -> None:
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(
        _build_markdown(
            generated_at=payload["generated_at"],
            chunking_strategy=payload["chunking_strategy"],
            cache_enabled=payload["cache_enabled"],
            summary=payload["summary"],
            samples=payload["samples"],
        ),
        encoding="utf-8",
    )

    print(f"Wrote JSON results to {output_json}")
    print(f"Wrote Markdown summary to {output_md}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RAGAS evaluation for the Claude Certification Assistant.")
    parser.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS_PATH)
    parser.add_argument("--chunking-strategy", default="hierarchical")
    parser.add_argument("--similarity-threshold", type=float, default=0.92)
    parser.add_argument("--use-cache", action="store_true", help="Allow semantic cache during evaluation.")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_RESULTS_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_RESULTS_MD)
    args = parser.parse_args()

    payload = run_evaluation(
        questions_path=args.questions,
        chunking_strategy=args.chunking_strategy,
        similarity_threshold=args.similarity_threshold,
        use_cache=args.use_cache,
    )
    write_evaluation_outputs(
        payload,
        output_json=args.output_json,
        output_md=args.output_md,
    )


if __name__ == "__main__":
    main()
