from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass
class ChunkingResult:
    parent_chunks: List[Document]
    child_chunks: List[Document]


def _looks_like_heading(line: str) -> bool:
    """
    Heuristic heading detection for structured docs / exported web pages / PDF text.
    """
    stripped = line.strip()
    if not stripped:
        return False

    # Markdown heading
    if stripped.startswith("#"):
        return True

    # Numbered heading: 1, 1.1, 2.3.4 etc.
    if re.match(r"^\d+(\.\d+)*[\)\.]?\s+[A-Z]", stripped):
        return True

    # ALL CAPS short heading
    if stripped.isupper() and 3 <= len(stripped) <= 90:
        return True

    # Title Case short line with no terminal punctuation
    words = stripped.split()
    if 2 <= len(words) <= 12 and stripped[-1] not in ".!?":
        titlecase_ratio = sum(1 for w in words if w[:1].isupper()) / max(len(words), 1)
        if titlecase_ratio >= 0.6:
            return True

    return False


def _split_document_into_sections(doc: Document) -> List[Document]:
    """
    Split a document into section-level parent candidates using heading-like lines.
    Falls back to one whole section if no headings are found.
    """
    text = doc.page_content or ""
    lines = text.splitlines()

    sections: List[Document] = []
    current_title = "Introduction"
    current_lines: List[str] = []
    section_index = 0
    found_heading = False

    for line in lines:
        if _looks_like_heading(line):
            found_heading = True
            if current_lines:
                section_text = "\n".join(current_lines).strip()
                if section_text:
                    metadata = {
                        **doc.metadata,
                        "section_title": current_title,
                        "section_index": section_index,
                    }
                    sections.append(Document(page_content=section_text, metadata=metadata))
                    section_index += 1
                current_lines = []

            current_title = line.strip()
        else:
            current_lines.append(line)

    if current_lines:
        section_text = "\n".join(current_lines).strip()
        if section_text:
            metadata = {
                **doc.metadata,
                "section_title": current_title,
                "section_index": section_index,
            }
            sections.append(Document(page_content=section_text, metadata=metadata))

    if not found_heading:
        return [
            Document(
                page_content=text,
                metadata={
                    **doc.metadata,
                    "section_title": "Full Document",
                    "section_index": 0,
                },
            )
        ]

    return sections


def _make_parent_id(metadata: dict, parent_index: int) -> str:
    source = metadata.get("source") or metadata.get("source_url") or "unknown"
    page = metadata.get("page_label") or metadata.get("page") or "na"
    section_index = metadata.get("section_index", 0)
    return f"{source}::p{page}::s{section_index}::parent{parent_index}"


def _recursive_chunks(
    documents: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    for idx, chunk in enumerate(chunks):
        chunk.metadata = {
            **chunk.metadata,
            "chunking_strategy": "recursive",
            "chunk_level": "child",
            "child_chunk_index": idx,
        }

    return chunks


def build_parent_child_chunks(
    documents: List[Document],
    parent_chunk_size: int = 1800,
    parent_chunk_overlap: int = 200,
    child_chunk_size: int = 700,
    child_chunk_overlap: int = 120,
) -> ChunkingResult:
    """
    Advanced chunking:
    1. split each doc into heading-aware sections
    2. split sections into larger parent chunks
    3. split parent chunks into smaller child chunks for retrieval
    """
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=parent_chunk_size,
        chunk_overlap=parent_chunk_overlap,
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=child_chunk_size,
        chunk_overlap=child_chunk_overlap,
    )

    parent_chunks: List[Document] = []
    child_chunks: List[Document] = []

    for doc in documents:
        section_docs = _split_document_into_sections(doc)

        for section_doc in section_docs:
            split_parents = parent_splitter.split_documents([section_doc])

            for parent_index, parent_doc in enumerate(split_parents):
                parent_id = _make_parent_id(parent_doc.metadata, parent_index)

                parent_doc.metadata = {
                    **parent_doc.metadata,
                    "parent_id": parent_id,
                    "chunking_strategy": "hierarchical_parent_child",
                    "chunk_level": "parent",
                    "parent_chunk_index": parent_index,
                }
                parent_chunks.append(parent_doc)

                split_children = child_splitter.split_documents([parent_doc])

                for child_index, child_doc in enumerate(split_children):
                    child_doc.metadata = {
                        **child_doc.metadata,
                        "parent_id": parent_id,
                        "chunking_strategy": "hierarchical_parent_child",
                        "chunk_level": "child",
                        "child_chunk_index": child_index,
                    }
                    child_chunks.append(child_doc)

    return ChunkingResult(
        parent_chunks=parent_chunks,
        child_chunks=child_chunks,
    )


def chunk_documents(
    documents: List[Document],
    strategy: str = "recursive",
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    parent_chunk_size: int = 1800,
    parent_chunk_overlap: int = 200,
    child_chunk_size: int = 700,
    child_chunk_overlap: int = 120,
) -> List[Document]:
    """
    Public entry point.

    Strategies:
    - recursive: baseline chunking
    - hierarchical: structure-aware parent-child chunking

    Returns retrieval-ready chunks.
    For hierarchical mode, returns child chunks.
    """
    strategy = strategy.lower().strip()

    if strategy == "recursive":
        return _recursive_chunks(
            documents=documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    if strategy == "hierarchical":
        result = build_parent_child_chunks(
            documents=documents,
            parent_chunk_size=parent_chunk_size,
            parent_chunk_overlap=parent_chunk_overlap,
            child_chunk_size=child_chunk_size,
            child_chunk_overlap=child_chunk_overlap,
        )
        return result.child_chunks

    raise ValueError(
        f"Unsupported chunking strategy: {strategy}. "
        "Use 'recursive' or 'hierarchical'."
    )