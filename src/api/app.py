"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes_search import router as search_router
from src.api.routes_tools import router as tools_router
from src.indexing.qdrant_store import QdrantStore
from src.retrieval.hybrid_search import HybridSearcher

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize shared resources on startup."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    logger.info("Loading models and connecting to Qdrant...")
    store = QdrantStore()
    store.ensure_collection()
    searcher = HybridSearcher(store)
    app.state.searcher = searcher
    app.state.store = store
    logger.info(f"Ready. Qdrant has {store.count()} points.")
    yield


app = FastAPI(
    title="Notion RAG Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(search_router, prefix="", tags=["search"])
app.include_router(tools_router, prefix="", tags=["tools"])


@app.get("/health")
def health():
    return {"status": "ok", "points": app.state.store.count()}
