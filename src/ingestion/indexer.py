from __future__ import annotations

import json
from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_chroma import Chroma

from src.ingestion.chunker import chunk_documents, build_parent_child_chunks
from src.model_config import get_embeddings

PERSIST_DIR = Path("data/chroma")
PARENT_STORE_PATH = PERSIST_DIR / "parent_store.json"

RECURSIVE_COLLECTION = "anthropic_rag_recursive"
HIERARCHICAL_COLLECTION = "anthropic_rag_hierarchical"


def _serialize_document(doc: Document) -> dict:
    return {
        "page_content": doc.page_content,
        "metadata": doc.metadata,
    }


def _save_parent_store(parent_chunks: List[Document]) -> None:
    parent_map = {}

    for parent_doc in parent_chunks:
        parent_id = parent_doc.metadata.get("parent_id")
        if not parent_id:
            continue
        parent_map[parent_id] = _serialize_document(parent_doc)

    PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    with open(PARENT_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(parent_map, f, ensure_ascii=False, indent=2)


def load_parent_store() -> dict:
    if not PARENT_STORE_PATH.exists():
        return {}

    with open(PARENT_STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _reset_collection(collection_name: str) -> None:
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(PERSIST_DIR),
    )
    vectorstore.delete_collection()


def _build_recursive_vectorstore(
    documents: List[Document],
    reset: bool = True,
) -> Chroma:
    chunks = chunk_documents(
        documents,
        strategy="recursive",
    )

    if reset:
        _reset_collection(RECURSIVE_COLLECTION)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=RECURSIVE_COLLECTION,
        persist_directory=str(PERSIST_DIR),
    )
    return vectorstore


def _build_hierarchical_vectorstore(
    documents: List[Document],
    reset: bool = True,
) -> Chroma:
    result = build_parent_child_chunks(documents)

    _save_parent_store(result.parent_chunks)

    if reset:
        _reset_collection(HIERARCHICAL_COLLECTION)

    vectorstore = Chroma.from_documents(
        documents=result.child_chunks,
        embedding=get_embeddings(),
        collection_name=HIERARCHICAL_COLLECTION,
        persist_directory=str(PERSIST_DIR),
    )
    return vectorstore


def build_vectorstore(
    documents: List[Document],
    strategy: str = "hierarchical",
    reset: bool = True,
) -> Chroma:
    """
    Build and persist vectorstore.

    recursive:
        index recursive chunks directly
    hierarchical:
        index child chunks and persist parent chunks separately
    """
    PERSIST_DIR.mkdir(parents=True, exist_ok=True)
    strategy = strategy.lower().strip()

    if strategy == "recursive":
        return _build_recursive_vectorstore(documents, reset=reset)

    if strategy == "hierarchical":
        return _build_hierarchical_vectorstore(documents, reset=reset)

    raise ValueError(
        f"Unsupported indexing strategy: {strategy}. "
        "Use 'recursive' or 'hierarchical'."
    )


def load_vectorstore(strategy: str = "hierarchical") -> Chroma:
    if not PERSIST_DIR.exists():
        raise FileNotFoundError(
            f"Chroma directory not found at {PERSIST_DIR}. Run ingestion first."
        )

    strategy = strategy.lower().strip()

    if strategy == "recursive":
        collection_name = RECURSIVE_COLLECTION
    elif strategy == "hierarchical":
        collection_name = HIERARCHICAL_COLLECTION
    else:
        raise ValueError(
            f"Unsupported indexing strategy: {strategy}. "
            "Use 'recursive' or 'hierarchical'."
        )

    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(PERSIST_DIR),
    )
