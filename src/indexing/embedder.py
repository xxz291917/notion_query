"""Embedding layer: dense (BGE-M3) + sparse (BM42) via FastEmbed."""

import logging
from typing import Iterator

from fastembed import SparseTextEmbedding, TextEmbedding

from src.config import settings

logger = logging.getLogger(__name__)


class Embedder:
    """Generates dense and sparse embeddings for text chunks."""

    def __init__(self):
        logger.info(f"Loading dense model: {settings.dense_model}")
        self.dense = TextEmbedding(
            model_name=settings.dense_model, cache_dir=settings.model_cache_dir
        )
        logger.info(f"Loading sparse model: {settings.sparse_model}")
        self.sparse = SparseTextEmbedding(
            model_name=settings.sparse_model, cache_dir=settings.model_cache_dir
        )

    def embed_dense(self, texts: list[str]) -> list[list[float]]:
        """Generate dense embeddings. Returns list of 1024-dim vectors."""
        return [vec.tolist() for vec in self.dense.embed(texts)]

    def embed_sparse(self, texts: list[str]) -> list[dict]:
        """Generate sparse embeddings. Returns list of {indices, values} dicts."""
        results = []
        for vec in self.sparse.embed(texts):
            results.append({
                "indices": vec.indices.tolist(),
                "values": vec.values.tolist(),
            })
        return results

    def embed_batch(
        self, texts: list[str], batch_size: int = 32
    ) -> Iterator[tuple[list[list[float]], list[dict]]]:
        """Yield (dense_vectors, sparse_vectors) for each batch of texts."""
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            dense = self.embed_dense(batch)
            sparse = self.embed_sparse(batch)
            yield dense, sparse
