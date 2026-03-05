"""Notion API client with pagination, rate limiting, and fault tolerance."""

import logging
from datetime import datetime
from typing import Any, Iterator

from notion_client import Client
from notion_client.errors import APIResponseError

from src.config import settings
from src.utils.fault_tolerance import CircuitBreaker, RateLimiter, RetryPolicy

logger = logging.getLogger(__name__)


class NotionClient:
    """Wraps the official Notion SDK with rate limiting and retry logic."""

    def __init__(self, token: str | None = None):
        self.client = Client(auth=token or settings.notion_token)
        self.rate_limiter = RateLimiter(rate=settings.notion_rate_limit)
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
        self.retry_policy = RetryPolicy(max_retries=3, base_delay=1.0)

    def _call(self, method, **kwargs) -> Any:
        """Execute a Notion API call with rate limiting, retry, and circuit breaker."""
        self.rate_limiter.acquire()

        @self.retry_policy.retry
        def _do_call():
            return self.circuit_breaker.call(method, **kwargs)

        return _do_call()

    # ── Discovery ──

    def list_databases(self) -> list[dict]:
        """List all databases accessible to the integration."""
        results = []
        response = self._call(
            self.client.search,
            filter={"property": "object", "value": "data_source"},
            page_size=100,
        )
        results.extend(response["results"])
        while response.get("has_more"):
            response = self._call(
                self.client.search,
                filter={"property": "object", "value": "data_source"},
                start_cursor=response["next_cursor"],
                page_size=100,
            )
            results.extend(response["results"])
        return results

    # ── Database query ──

    def query_database(
        self,
        database_id: str,
        filter: dict | None = None,
        sorts: list | None = None,
    ) -> Iterator[dict]:
        """Yield all pages from a database, handling pagination."""
        kwargs: dict[str, Any] = {"data_source_id": database_id, "page_size": 100}
        if filter:
            kwargs["filter"] = filter
        if sorts:
            kwargs["sorts"] = sorts

        while True:
            response = self._call(self.client.data_sources.query, **kwargs)
            yield from response["results"]
            if not response.get("has_more"):
                break
            kwargs["start_cursor"] = response["next_cursor"]

    def query_database_since(
        self, database_id: str, since: datetime
    ) -> Iterator[dict]:
        """Query pages edited after a given timestamp (for incremental sync)."""
        yield from self.query_database(
            database_id,
            filter={
                "timestamp": "last_edited_time",
                "last_edited_time": {"after": since.isoformat()},
            },
            sorts=[{"timestamp": "last_edited_time", "direction": "descending"}],
        )

    # ── Page content ──

    def get_page(self, page_id: str) -> dict:
        return self._call(self.client.pages.retrieve, page_id=page_id)

    def get_blocks(self, block_id: str) -> list[dict]:
        """Recursively fetch all blocks for a page."""
        blocks = []
        kwargs: dict[str, Any] = {"block_id": block_id, "page_size": 100}
        while True:
            response = self._call(self.client.blocks.children.list, **kwargs)
            for block in response["results"]:
                blocks.append(block)
                if block.get("has_children"):
                    block["children"] = self.get_blocks(block["id"])
            if not response.get("has_more"):
                break
            kwargs["start_cursor"] = response["next_cursor"]
        return blocks

    # ── Database metadata ──

    def get_database(self, database_id: str) -> dict:
        return self._call(self.client.databases.retrieve, database_id=database_id)
