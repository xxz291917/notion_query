"""General search endpoints: /search and /query."""

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    db_type: str | None = Field(default=None, description="Filter by database type")
    rerank: bool = True


class SearchResult(BaseModel):
    chunk_id: str
    text: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    results: list[SearchResult]
    total: int


@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest, request: Request):
    """Hybrid search: returns relevant chunks with scores and source links."""
    searcher = request.app.state.searcher
    results = searcher.search(
        query=req.query,
        top_k=req.top_k,
        db_type=req.db_type,
        rerank=req.rerank,
    )
    return SearchResponse(
        results=[
            SearchResult(
                chunk_id=r["chunk_id"],
                text=r["text"],
                score=r.get("rerank_score", r.get("score", 0)),
                metadata=r.get("metadata", {}),
            )
            for r in results
        ],
        total=len(results),
    )
