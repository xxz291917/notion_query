"""MCP server: exposes Notion RAG search as MCP tools via REST API proxy.

Lightweight — no model loading. Calls the FastAPI server over HTTP.
Requires API_BASE_URL (default http://localhost:8900) and API_KEY env vars.
"""

import json
import os
import urllib.request

from mcp.server.fastmcp import FastMCP

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8900")
API_KEY = os.environ.get("API_KEY", "")

mcp = FastMCP(
    "Notion RAG",
    instructions=(
        "Search the company Notion workspace knowledge base. "
        "Use the search tool to find problems, bugs, solutions, projects, tasks, "
        "documents, and people information."
    ),
)


def _api_call(path: str, body: dict) -> list[dict]:
    """Call the REST API and return results."""
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    req = urllib.request.Request(f"{API_BASE_URL}{path}", data=data, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["results"]


@mcp.tool()
def search(
    query: str,
    db_type: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    """Search the Notion knowledge base with hybrid (dense + sparse) retrieval and reranking.

    Args:
        query: Natural language search query (supports Chinese and English).
        db_type: Filter by database type. Options: problems, solutions, projects,
                 tasks, bugs, documents, designs, deliverables, feedback, people.
                 Leave empty to search all.
        top_k: Number of results to return (1-20, default 5).
    """
    top_k = max(1, min(top_k, 20))
    body: dict = {"query": query, "top_k": top_k}
    if db_type:
        body["db_type"] = db_type
    results = _api_call("/search", body)
    return [
        {
            "title": r.get("metadata", {}).get("title", ""),
            "text": r["text"],
            "url": r.get("metadata", {}).get("url", ""),
            "score": r.get("score", 0),
            "db_type": r.get("metadata", {}).get("db_type", ""),
            "status": r.get("metadata", {}).get("status", ""),
        }
        for r in results
    ]


@mcp.tool()
def search_problems(query: str, top_k: int = 5) -> list[dict]:
    """Search the Problems database for known issues and their status/stage."""
    return search(query=query, db_type="problems", top_k=top_k)


@mcp.tool()
def search_bugs(query: str, top_k: int = 5) -> list[dict]:
    """Search the Bugs database for bug reports by severity/project."""
    return search(query=query, db_type="bugs", top_k=top_k)


@mcp.tool()
def search_solutions(query: str, top_k: int = 5) -> list[dict]:
    """Search the Solutions database for implemented fixes and proposals."""
    return search(query=query, db_type="solutions", top_k=top_k)


@mcp.tool()
def search_docs(query: str, top_k: int = 5) -> list[dict]:
    """Search Documents (RCA reports, Wiki, strategies, technical docs)."""
    return search(query=query, db_type="documents", top_k=top_k)


@mcp.tool()
def search_tasks(query: str, top_k: int = 5) -> list[dict]:
    """Search the Tasks database for work items and assignments."""
    return search(query=query, db_type="tasks", top_k=top_k)


@mcp.tool()
def search_people(query: str, top_k: int = 5) -> list[dict]:
    """Search People and their Areas of Responsibility (AOR)."""
    return search(query=query, db_type="people", top_k=top_k)


if __name__ == "__main__":
    mcp.run()
