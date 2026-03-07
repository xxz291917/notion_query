"""General search endpoints: /search and /query."""

import logging
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    db_type: str | None = Field(default=None, description="Filter by database type")
    filters: dict[str, str] | None = Field(
        default=None,
        description="Field filters: status, owner, type, scope. E.g. {\"status\": \"In progress\"}",
    )
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
def search(req: SearchRequest, request: Request) -> SearchResponse:
    """Hybrid search: returns relevant chunks with scores and source links.

    Performs a hybrid search combining semantic and keyword-based search,
    with optional reranking for improved relevance.

    Args:
        req (SearchRequest): The search request containing:
            - query: The search query string
            - top_k: Number of results to return (1-50, default 5)
            - db_type: Optional database type filter
            - filters: Optional field filters (status, owner, type, scope)
            - rerank: Whether to apply reranking (default True)
        request (Request): FastAPI request object containing app state

    Returns:
        SearchResponse: Search results containing:
            - results: List of SearchResult objects with chunk_id, text, score, and metadata
            - total: Total number of results returned

    Raises:
        HTTPException: If search operation fails or searcher is not initialized
    """
    logger.info(
        f"Search request: query='{req.query}', top_k={req.top_k}, "
        f"db_type={req.db_type}, rerank={req.rerank}"
    )

    try:
        searcher = request.app.state.searcher
        if searcher is None:
            logger.error("Searcher not initialized in app state")
            raise HTTPException(
                status_code=500,
                detail="Search service not initialized"
            )

        results = searcher.search(
            query=req.query,
            top_k=req.top_k,
            db_type=req.db_type,
            filters=req.filters,
            rerank=req.rerank,
        )

        logger.info(f"Search completed successfully, found {len(results)} results")

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

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.exception(f"Search failed for query '{req.query}': {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Search operation failed: {str(e)}"
        )
