"""Sync engine: pull Notion data, chunk, embed, and upsert into Qdrant.

Supports checkpoint/resume: tracks per-page and per-database progress so
interrupted syncs can continue from where they left off.
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from src.config import settings
from src.indexing.chunker import chunk_document
from src.indexing.embedder import Embedder
from src.indexing.qdrant_store import QdrantStore
from src.notion.client import NotionClient
from src.notion.extractor import page_to_document

logger = logging.getLogger(__name__)

STATE_FILE = Path("data/sync_state.json")


class SyncEngine:
    """Orchestrates full and incremental syncs from Notion to Qdrant."""

    def __init__(self):
        self.notion = NotionClient()
        self.embedder = Embedder()
        self.store = QdrantStore()

    def full_sync(self, database_ids: dict[str, str] | None = None) -> int:
        """Full sync with checkpoint/resume support.

        If a previous full sync was interrupted, resumes from where it left off
        (skipping already-synced pages and completed databases).
        """
        self.store.ensure_collection()

        if database_ids is None:
            database_ids = self._discover_databases()

        state = self._load_state()
        progress = state.get("in_progress")

        # Resume check: only resume if same mode
        if progress and progress.get("mode") == "full":
            synced_pages = set(progress.get("synced_pages", []))
            completed_dbs = set(progress.get("completed_dbs", []))
            logger.info(
                f"Resuming full sync: {len(synced_pages)} pages synced, "
                f"{len(completed_dbs)} databases completed"
            )
        else:
            synced_pages = set()
            completed_dbs = set()
            self._save_in_progress(state, "full", synced_pages, completed_dbs)

        total_chunks = 0
        for db_name, db_id in database_ids.items():
            if db_name in completed_dbs:
                logger.info(f"Skipping completed database: {db_name}")
                continue

            logger.info(f"Syncing database: {db_name} ({db_id})")
            count = self._sync_database(db_name, db_id, synced_pages=synced_pages)
            total_chunks += count
            logger.info(f"  {db_name}: {count} chunks indexed")

            completed_dbs.add(db_name)
            synced_pages.clear()  # completed_dbs already skips this db on resume
            state = self._load_state()
            self._save_in_progress(state, "full", synced_pages, completed_dbs)

        self._finish_sync()
        logger.info(f"Full sync complete. Total chunks: {total_chunks}")
        return total_chunks

    def incremental_sync(self, database_ids: dict[str, str] | None = None) -> int:
        """Incremental sync with checkpoint/resume support."""
        self.store.ensure_collection()

        state = self._load_state()
        progress = state.get("in_progress")

        # Determine the 'since' timestamp
        if progress and progress.get("mode") == "incremental":
            since = datetime.fromisoformat(progress["since"])
            synced_pages = set(progress.get("synced_pages", []))
            completed_dbs = set(progress.get("completed_dbs", []))
            logger.info(
                f"Resuming incremental sync (since {since.isoformat()}): "
                f"{len(synced_pages)} pages synced, {len(completed_dbs)} dbs completed"
            )
        else:
            last_sync = state.get("last_sync")
            if last_sync is None:
                logger.info("No previous sync state found, running full sync")
                return self.full_sync(database_ids)
            since = datetime.fromisoformat(last_sync)
            synced_pages = set()
            completed_dbs = set()

        if database_ids is None:
            database_ids = self._discover_databases()

        # Save in_progress with the 'since' timestamp so resume uses the same baseline
        self._save_in_progress(
            state, "incremental", synced_pages, completed_dbs, since=since
        )

        total_chunks = 0
        for db_name, db_id in database_ids.items():
            if db_name in completed_dbs:
                logger.info(f"Skipping completed database: {db_name}")
                continue

            logger.info(f"Incremental sync: {db_name} (since {since.isoformat()})")
            count = self._sync_database(
                db_name, db_id, since=since, synced_pages=synced_pages
            )
            total_chunks += count

            completed_dbs.add(db_name)
            synced_pages.clear()
            state = self._load_state()
            self._save_in_progress(
                state, "incremental", synced_pages, completed_dbs, since=since
            )

        self._finish_sync()
        logger.info(f"Incremental sync complete. Updated chunks: {total_chunks}")
        return total_chunks

    def _sync_database(
        self,
        db_name: str,
        db_id: str,
        since: datetime | None = None,
        synced_pages: set[str] | None = None,
    ) -> int:
        """Sync a single database. Returns number of chunks indexed."""
        if synced_pages is None:
            synced_pages = set()

        if since:
            pages = self.notion.query_database_since(db_id, since)
        else:
            pages = self.notion.query_database(db_id)

        total = 0
        batch_chunks: list[dict] = []
        batch_page_ids: list[str] = []

        for page in pages:
            notion_id = page["id"]

            if notion_id in synced_pages:
                logger.debug(f"Skipping already-synced page {notion_id}")
                continue

            try:
                md = self.notion.get_page_markdown(notion_id)
                doc = page_to_document(page, md, db_name=db_name)
                chunks = chunk_document(doc)

                if not chunks:
                    synced_pages.add(notion_id)
                    continue

                if since:
                    self.store.delete_by_notion_id(notion_id)

                batch_chunks.extend(chunks)
                batch_page_ids.append(notion_id)

                # Flush batch when large enough
                if len(batch_chunks) >= 32:
                    total += self._embed_and_upsert(batch_chunks)
                    synced_pages.update(batch_page_ids)
                    self._save_page_progress(synced_pages)
                    batch_chunks = []
                    batch_page_ids = []

            except Exception:
                logger.exception(f"Failed to sync page {notion_id}")

        # Flush remaining
        if batch_chunks:
            total += self._embed_and_upsert(batch_chunks)
            synced_pages.update(batch_page_ids)
            self._save_page_progress(synced_pages)

        return total

    def _embed_and_upsert(self, chunks: list[dict]) -> int:
        """Embed a batch of chunks and upsert into Qdrant."""
        texts = [c["text"] for c in chunks]
        dense_vecs = self.embedder.embed_dense(texts)
        sparse_vecs = self.embedder.embed_sparse(texts)
        self.store.upsert_chunks(chunks, dense_vecs, sparse_vecs)
        return len(chunks)

    # ── Checkpoint persistence ──

    def _load_state(self) -> dict:
        if not STATE_FILE.exists():
            return {}
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return {}

    def _save_state(self, state: dict) -> None:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

    def _save_in_progress(
        self,
        state: dict,
        mode: str,
        synced_pages: set[str],
        completed_dbs: set[str],
        since: datetime | None = None,
    ) -> None:
        """Save current sync progress to state file."""
        progress = {
            "mode": mode,
            "started_at": state.get("in_progress", {}).get(
                "started_at", datetime.now(UTC).isoformat()
            ),
            "synced_pages": list(synced_pages),
            "completed_dbs": list(completed_dbs),
        }
        if since:
            progress["since"] = since.isoformat()
        state["in_progress"] = progress
        self._save_state(state)

    def _save_page_progress(self, synced_pages: set[str]) -> None:
        """Quick update: only update synced_pages in current in_progress state."""
        state = self._load_state()
        if state.get("in_progress"):
            state["in_progress"]["synced_pages"] = list(synced_pages)
            self._save_state(state)

    def _finish_sync(self) -> None:
        """Mark sync as complete: update last_sync and clear in_progress."""
        state = self._load_state()
        state["last_sync"] = datetime.now(UTC).isoformat()
        state.pop("in_progress", None)
        self._save_state(state)

    # ── Database discovery ──

    CORE_DB_TYPES = {
        "problems", "solutions", "projects", "tasks", "bugs",
        "documents", "designs", "deliverables", "feedback",
        "responsibilities", "people",
    }

    def _discover_databases(self) -> dict[str, str]:
        """Auto-discover all databases and use their titles as names."""
        databases = self.notion.list_databases()
        result = {}
        for db in databases:
            title_parts = db.get("title", [])
            name = "".join(t.get("plain_text", "") for t in title_parts) or db["id"]
            db_type = name.lower().replace(" ", "_").replace("database", "").strip("_")
            key = db_type or db["id"]
            result[key] = db["id"]

        filtered = {k: v for k, v in result.items() if k in self.CORE_DB_TYPES}
        skipped = set(result.keys()) - set(filtered.keys())
        if skipped:
            logger.info(f"Skipping non-core databases: {skipped}")
        logger.info(f"Discovered {len(filtered)} core databases: {list(filtered.keys())}")
        return filtered
