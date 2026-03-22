from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, WebBaseLoader


def _normalize_paths(paths: Iterable[str | Path]) -> list[Path]:
    return [Path(p).resolve() for p in paths]


def discover_raw_documents(
    raw_dir: str | Path,
    include_md: bool = True,
    include_pdf: bool = True,
) -> dict[str, list[Path]]:
    """
    Discover local corpus files from a raw data folder.
    """
    raw_path = Path(raw_dir).resolve()
    if not raw_path.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_path}")

    md_files = sorted(raw_path.glob("*.md")) if include_md else []
    pdf_files = sorted(raw_path.glob("*.pdf")) if include_pdf else []

    return {
        "md_paths": md_files,
        "pdf_paths": pdf_files,
    }


def load_web_documents(urls: list[str]) -> List[Document]:
    docs: List[Document] = []

    for url in urls:
        loader = WebBaseLoader(url)
        loaded = loader.load()

        for doc in loaded:
            doc.metadata["source_type"] = "web"
            doc.metadata["source_url"] = url

        docs.extend(loaded)

    return docs


def load_pdf_documents(pdf_paths: list[str | Path]) -> List[Document]:
    docs: List[Document] = []

    for pdf_path in _normalize_paths(pdf_paths):
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        loader = PyPDFLoader(str(pdf_path))
        loaded = loader.load()

        for doc in loaded:
            doc.metadata["source_type"] = "pdf"
            doc.metadata["file_name"] = pdf_path.name

        docs.extend(loaded)

    return docs


def load_markdown_documents(md_paths: list[str | Path]) -> List[Document]:
    docs: List[Document] = []

    for md_path in _normalize_paths(md_paths):
        if not md_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        loader = TextLoader(str(md_path), encoding="utf-8")
        loaded = loader.load()

        for doc in loaded:
            doc.metadata["source_type"] = "markdown"
            doc.metadata["file_name"] = md_path.name
            doc.metadata["source"] = str(md_path)

        docs.extend(loaded)

    return docs


def load_all_documents(
    urls: list[str] | None = None,
    pdf_paths: list[str | Path] | None = None,
    md_paths: list[str | Path] | None = None,
) -> List[Document]:
    """
    Load web, PDF, and markdown documents into one corpus.
    """
    urls = urls or []
    pdf_paths = pdf_paths or []
    md_paths = md_paths or []

    web_docs = load_web_documents(urls) if urls else []
    pdf_docs = load_pdf_documents(pdf_paths) if pdf_paths else []
    md_docs = load_markdown_documents(md_paths) if md_paths else []

    return web_docs + pdf_docs + md_docs