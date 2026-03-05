"""Specialized tool endpoints for Agent function calling."""

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class ToolSearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    status: str | None = None
    priority: str | None = None


class ToolResult(BaseModel):
    title: str
    text: str
    url: str
    score: float
    properties: dict


class ToolSearchResponse(BaseModel):
    results: list[ToolResult]


def _tool_search(request: Request, req: ToolSearchRequest, db_type: str) -> ToolSearchResponse:
    """Shared logic for specialized tool endpoints."""
    searcher = request.app.state.searcher
    results = searcher.search(query=req.query, top_k=req.top_k, db_type=db_type)

    tool_results = []
    for r in results:
        meta = r.get("metadata", {})
        # Apply post-filters on structured fields
        if req.status and meta.get("status", "").lower() != req.status.lower():
            continue
        if req.priority and meta.get("priority", "").lower() != req.priority.lower():
            continue
        tool_results.append(
            ToolResult(
                title=meta.get("title", ""),
                text=r["text"],
                url=meta.get("url", ""),
                score=r.get("rerank_score", r.get("score", 0)),
                properties={k: v for k, v in meta.items() if k not in ("text", "chunk_id")},
            )
        )
    return ToolSearchResponse(results=tool_results)


@router.post("/search/problems", response_model=ToolSearchResponse)
def search_problems(req: ToolSearchRequest, request: Request):
    """Search the Problems database by status/stage."""
    return _tool_search(request, req, db_type="problems")


@router.post("/search/bugs", response_model=ToolSearchResponse)
def search_bugs(req: ToolSearchRequest, request: Request):
    """Search the Bugs database by severity/project."""
    return _tool_search(request, req, db_type="bugs")


@router.post("/search/docs", response_model=ToolSearchResponse)
def search_docs(req: ToolSearchRequest, request: Request):
    """Search Documents (RCA, Wiki, strategies)."""
    return _tool_search(request, req, db_type="documents")


@router.post("/search/people", response_model=ToolSearchResponse)
def search_people(req: ToolSearchRequest, request: Request):
    """Search People and AOR responsibilities."""
    return _tool_search(request, req, db_type="people")


@router.post("/search/tasks", response_model=ToolSearchResponse)
def search_tasks(req: ToolSearchRequest, request: Request):
    """Search Tasks database."""
    return _tool_search(request, req, db_type="tasks")


@router.post("/search/solutions", response_model=ToolSearchResponse)
def search_solutions(req: ToolSearchRequest, request: Request):
    """Search Solutions database."""
    return _tool_search(request, req, db_type="solutions")
