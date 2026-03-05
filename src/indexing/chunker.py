"""Chunking strategy: structured DB records stay whole, long documents get split."""

import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import settings

logger = logging.getLogger(__name__)

# DB types whose records are short enough to keep as single chunks
STRUCTURED_DB_TYPES = {
    "problems", "solutions", "tasks", "bugs", "deliverables",
    "projects", "feedback", "responsibilities", "people",
}

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
    separators=["\n## ", "\n### ", "\n```", "\n\n", "\n", ". ", " "],
    length_function=len,  # character-based; token-based needs tiktoken
)


def chunk_document(doc: dict) -> list[dict]:
    """Split a document into chunks for indexing.

    Args:
        doc: Output from page_to_document(), must have 'content', 'notion_id', etc.

    Returns:
        List of chunk dicts, each with 'chunk_id', 'text', 'metadata'.
    """
    db_type = (doc.get("db_type") or "").lower()
    content = doc.get("content", "")
    notion_id = doc["notion_id"]

    # Shared metadata for all chunks from this page
    base_meta = {
        "notion_id": notion_id,
        "title": doc.get("title", ""),
        "url": doc.get("url", ""),
        "db_type": db_type,
        "last_edited": doc.get("last_edited", ""),
    }
    # Add filterable structured properties
    props = doc.get("properties", {})
    for key in ("Status", "Priority", "Assignee", "Owner", "Scope", "Type"):
        val = props.get(key)
        if val is not None and val != "" and val != []:
            base_meta[key.lower()] = val

    if not content.strip():
        return []

    # Structured DB records: keep as single chunk
    if db_type in STRUCTURED_DB_TYPES and len(content) < settings.chunk_size * 2:
        return [_make_chunk(notion_id, 0, content, base_meta)]

    # Long documents: recursive split
    texts = _splitter.split_text(content)
    return [_make_chunk(notion_id, i, text, base_meta) for i, text in enumerate(texts)]


def _make_chunk(notion_id: str, index: int, text: str, base_meta: dict) -> dict:
    return {
        "chunk_id": f"{notion_id}#{index}",
        "text": text,
        "metadata": {**base_meta, "chunk_index": index},
    }
