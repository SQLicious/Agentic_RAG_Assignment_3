from __future__ import annotations

import hashlib
import json
import math
import os
import sqlite3
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from src.model_config import get_embeddings

load_dotenv()

CACHE_DIR = Path("data/cache")
CACHE_DB_PATH = CACHE_DIR / "semantic_cache.db"
RAW_DIR = Path("data/raw")

TIME_SENSITIVE_TERMS = [
    "recent",
    "recently",
    "latest",
    "new",
    "launched",
    "announced",
    "current",
    "today",
    "this week",
    "this month",
    "now",
]


def normalize_question(question: str) -> str:
    return " ".join(question.strip().lower().split())


def is_time_sensitive_question(question: str) -> bool:
    q = normalize_question(question)
    return any(term in q for term in TIME_SENSITIVE_TERMS)


def compute_corpus_version(
    raw_dir: str | Path = RAW_DIR,
    chunking_strategy: str = "hierarchical",
) -> str:
    """
    Build a stable corpus fingerprint from:
    - file names
    - file sizes
    - modification times
    - chunking strategy
    """
    raw_path = Path(raw_dir)
    hasher = hashlib.sha256()
    hasher.update(chunking_strategy.encode("utf-8"))

    if not raw_path.exists():
        hasher.update(b"missing_raw_dir")
        return hasher.hexdigest()

    for path in sorted(raw_path.glob("*")):
        if path.is_file():
            stat = path.stat()
            payload = f"{path.name}|{stat.st_size}|{int(stat.st_mtime)}"
            hasher.update(payload.encode("utf-8"))

    return hasher.hexdigest()


def _cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


class SemanticCache:
    def __init__(self, db_path: str | Path = CACHE_DB_PATH):
        self.db_path = Path(db_path)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self.embeddings = get_embeddings()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS semantic_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    normalized_question TEXT NOT NULL,
                    embedding_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    corpus_version TEXT NOT NULL,
                    chunking_strategy TEXT NOT NULL,
                    hit_count INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def _embed_question(self, question: str) -> list[float]:
        normalized = normalize_question(question)
        return self.embeddings.embed_query(normalized)

    def get_similar(
        self,
        question: str,
        corpus_version: str,
        chunking_strategy: str = "hierarchical",
        similarity_threshold: float = 0.92,
    ) -> dict[str, Any] | None:
        """
        Return the best cache hit if similarity >= threshold
        and corpus/chunking match.
        """
        normalized_question = normalize_question(question)
        query_embedding = self._embed_question(normalized_question)

        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT id, question, normalized_question, embedding_json, result_json, hit_count
                FROM semantic_cache
                WHERE corpus_version = ?
                  AND chunking_strategy = ?
                """,
                (corpus_version, chunking_strategy),
            ).fetchall()

        best_match = None
        best_similarity = -1.0

        for row in rows:
            cached_embedding = json.loads(row["embedding_json"])
            similarity = _cosine_similarity(query_embedding, cached_embedding)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = row

        if best_match is None or best_similarity < similarity_threshold:
            return None

        with self._get_conn() as conn:
            conn.execute(
                """
                UPDATE semantic_cache
                SET hit_count = hit_count + 1
                WHERE id = ?
                """,
                (best_match["id"],),
            )
            conn.commit()

        cached_result = json.loads(best_match["result_json"])
        cached_result["cache_hit"] = True
        cached_result["cache_similarity"] = round(best_similarity, 4)
        cached_result["cache_source_question"] = best_match["question"]

        return cached_result

    def store(
        self,
        question: str,
        result: dict[str, Any],
        corpus_version: str,
        chunking_strategy: str = "hierarchical",
    ) -> None:
        """
        Store the final user-facing result for future semantic reuse.
        """
        normalized_question = normalize_question(question)
        embedding = self._embed_question(normalized_question)

        stored_result = {
            **result,
            "cache_hit": False,
            "cache_similarity": None,
            "cache_source_question": None,
        }

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO semantic_cache (
                    question,
                    normalized_question,
                    embedding_json,
                    result_json,
                    corpus_version,
                    chunking_strategy
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    question,
                    normalized_question,
                    json.dumps(embedding),
                    json.dumps(stored_result, ensure_ascii=False),
                    corpus_version,
                    chunking_strategy,
                ),
            )
            conn.commit()
