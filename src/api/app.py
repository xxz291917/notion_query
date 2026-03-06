"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routes_search import router as search_router
from src.api.routes_tools import router as tools_router
from src.config import settings
from src.indexing.qdrant_store import QdrantStore
from src.retrieval.hybrid_search import HybridSearcher

logger = logging.getLogger(__name__)

OPEN_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}


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
    if settings.api_key:
        logger.info("API key authentication enabled")
    else:
        logger.warning("No API_KEY set — all endpoints are unauthenticated!")
    logger.info(f"Ready. Qdrant has {store.count()} points.")
    yield


app = FastAPI(
    title="Notion RAG Service",
    version="0.1.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if not settings.api_key or request.url.path in OPEN_PATHS:
        return await call_next(request)
    auth = request.headers.get("Authorization", "")
    if auth == f"Bearer {settings.api_key}":
        return await call_next(request)
    return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key"})


app.include_router(search_router, prefix="", tags=["search"])
app.include_router(tools_router, prefix="", tags=["tools"])


@app.get("/health")
def health():
    return {"status": "ok", "points": app.state.store.count()}
