"""MCP server: exposes Notion RAG search as MCP tools via Streamable HTTP.

Lightweight — no model loading. Calls the FastAPI server over HTTP.
Env vars: API_BASE_URL, API_KEY (shared for backend API and MCP auth).
"""

import os

import httpx
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp.server.fastmcp import FastMCP

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8900")
API_KEY = os.environ.get("API_KEY", "")

MCP_HOST = os.environ.get("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.environ.get("MCP_PORT", "8950"))

mcp = FastMCP(
    "Notion RAG",
    instructions=(
        "Search the company Notion workspace knowledge base. "
        "Use the search tool to find problems, bugs, solutions, projects, tasks, "
        "documents, and people information."
    ),
    host=MCP_HOST,
    port=MCP_PORT,
)

_client: httpx.AsyncClient | None = None


def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        headers = {"Content-Type": "application/json"}
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        _client = httpx.AsyncClient(base_url=API_BASE_URL, headers=headers, timeout=30)
    return _client


async def _api_call(path: str, body: dict) -> list[dict]:
    """Call the REST API and return results."""
    try:
        resp = await _get_client().post(path, json=body)
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        return [{"error": f"API returned {e.response.status_code}: {e.response.text}"}]
    except httpx.RequestError as e:
        return [{"error": f"API request failed: {e}"}]
    data = resp.json()
    return data.get("results", [])


@mcp.tool()
async def search(
    query: str,
    db_type: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    """Search the Notion knowledge base with hybrid (dense + sparse) retrieval and reranking.

    Args:
        query: Natural language search query (supports Chinese and English).
        db_type: Filter by database type. Options: problems, solutions, projects,
                 tasks, bugs, documents, designs, feedback, people, responsibilities.
                 Leave empty to search all.
        status: Filter by status. Examples: "In progress", "Done", "1-Not started".
        owner: Filter by owner name. Examples: "Joseph Zeng", "Eva Liu".
        top_k: Number of results to return (1-20, default 5).
    """
    top_k = max(1, min(top_k, 20))
    body: dict = {"query": query, "top_k": top_k}
    if db_type:
        body["db_type"] = db_type
    filters = {}
    if status:
        filters["status"] = status
    if owner:
        filters["owner"] = owner
    if filters:
        body["filters"] = filters
    results = await _api_call("/search", body)
    if results and "error" in results[0]:
        return results
    return [
        {
            "title": r.get("metadata", {}).get("title", ""),
            "text": r.get("text", ""),
            "url": r.get("metadata", {}).get("url", ""),
            "score": r.get("score", 0),
            "db_type": r.get("metadata", {}).get("db_type", ""),
            "status": r.get("metadata", {}).get("status", ""),
            "owner": r.get("metadata", {}).get("owner", ""),
        }
        for r in results
    ]


class BearerAuthMiddleware(BaseHTTPMiddleware):
    """Simple bearer token auth middleware for MCP server."""

    async def dispatch(self, request: Request, call_next):
        if not API_KEY:
            return await call_next(request)
        auth = request.headers.get("Authorization", "")
        if auth == f"Bearer {API_KEY}":
            return await call_next(request)
        return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key"})


if __name__ == "__main__":
    app = mcp.streamable_http_app()
    app.add_middleware(BearerAuthMiddleware)
    uvicorn.run(app, host=MCP_HOST, port=MCP_PORT)
