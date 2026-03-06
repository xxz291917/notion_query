from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Notion
    notion_token: str = ""

    # Model cache (relative to project root)
    model_cache_dir: str = str(PROJECT_ROOT / "models")

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "notion_rag"

    # Embedding models
    dense_model: str = "intfloat/multilingual-e5-large"
    sparse_model: str = "Qdrant/bm42-all-minilm-l6-v2-attentions"
    reranker_model: str = "jinaai/jina-reranker-v2-base-multilingual"

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Retrieval
    search_top_k: int = 20
    rerank_top_k: int = 5

    # Sync
    sync_interval_minutes: int = 60
    notion_rate_limit: float = 3.0  # requests per second

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: str = ""  # set via API_KEY env var; empty = no auth

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
