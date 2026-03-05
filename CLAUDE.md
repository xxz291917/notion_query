# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Notion RAG service: syncs company Notion workspace data into a Qdrant vector database and exposes hybrid search (dense + sparse + reranker) via FastAPI. Designed to serve AI agents and OpenClaw.

## Commands

```bash
# Install
pip install -e .            # production deps
pip install -e ".[dev]"     # + pytest, httpx, ruff

# Qdrant (required for sync and API)
docker compose up -d qdrant

# Sync Notion data
python scripts/full_sync.py --mode discover      # list accessible databases
python scripts/full_sync.py --mode full           # full sync
python scripts/full_sync.py --mode incremental    # delta sync since last run

# Run API server
uvicorn src.api.app:app --reload

# Lint
ruff check src/ scripts/
ruff format src/ scripts/
```

## Architecture

Four-layer pipeline: **Notion extraction -> Indexing -> Retrieval -> API**

**Data flow:** Notion API -> `NotionClient` (rate-limited, circuit-breaker protected) -> `extractor` (properties -> metadata) + `block_parser` (blocks -> markdown) -> `chunker` (structured records kept whole, long docs split recursively) -> `Embedder` (FastEmbed: BGE-M3 dense 1024d + BM42 sparse) -> `QdrantStore` (dual-vector upsert with deterministic UUIDs)

**Search flow:** Query -> `HybridSearcher` encodes query with both models -> parallel dense + sparse search in Qdrant -> RRF fusion (no weight tuning) -> CrossEncoder rerank (BGE-Reranker-v2-m3) -> top-K results

**Key design decisions:**
- All embeddings via FastEmbed (ONNX, no PyTorch). Dense, sparse, and reranker all in one library.
- Structured DB records (tasks, bugs, etc.) are indexed as single chunks with properties in metadata for filtered search. Only long documents get split.
- `chunk_id = "{notion_id}#{index}"` with deterministic UUID5 for idempotent upserts.
- Incremental sync: delete old chunks by `notion_id` filter, then re-insert. State tracked in `data/sync_state.json`.

## Configuration

All config via env vars or `.env` file, managed by `src/config.py` (pydantic-settings). Key vars: `NOTION_TOKEN`, `QDRANT_HOST`, `QDRANT_PORT`, `DENSE_MODEL`, `SPARSE_MODEL`, `RERANKER_MODEL`.

## Conventions

- Python >=3.11, ruff for linting (line-length 100)
- All Notion API calls go through `src/notion/client.py` which enforces rate limiting (3 req/s) and circuit breaker
- Imports use `src.` prefix (e.g., `from src.config import settings`)
