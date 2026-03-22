from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.loader import discover_raw_documents, load_all_documents
from src.ingestion.indexer import build_vectorstore

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

discovered = discover_raw_documents(RAW_DIR)

docs = load_all_documents(
    urls=[],
    pdf_paths=discovered["pdf_paths"],
    md_paths=discovered["md_paths"],
)

vs = build_vectorstore(
    documents=docs,
    strategy="hierarchical",   # switch to "recursive" for baseline ablation
)

print(f"Raw directory: {RAW_DIR}")
print(f"Markdown files found: {len(discovered['md_paths'])}")
print(f"PDF files found: {len(discovered['pdf_paths'])}")
print(f"Loaded docs: {len(docs)}")
print("Built vectorstore successfully.")