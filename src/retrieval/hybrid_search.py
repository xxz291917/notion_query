"""Hybrid search with RRF fusion and cross-encoder reranking."""

import logging

from fastembed import TextEmbedding, SparseTextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder

from src.config import settings
from src.indexing.qdrant_store import QdrantStore

logger = logging.getLogger(__name__)


class HybridSearcher:
    """Performs hybrid (dense + sparse) search with RRF fusion and reranking."""

    def __init__(self, store: QdrantStore):
        self.store = store
        self.dense_model = TextEmbedding(
            model_name=settings.dense_model, cache_dir=settings.model_cache_dir
        )
        self.sparse_model = SparseTextEmbedding(
            model_name=settings.sparse_model, cache_dir=settings.model_cache_dir
        )
        self.reranker = TextCrossEncoder(
            model_name=settings.reranker_model, cache_dir=settings.model_cache_dir
        )

    def search(
        self,
        query: str,
        top_k: int | None = None,
        db_type: str | None = None,
        filters: dict[str, str] | None = None,
        rerank: bool = True,
    ) -> list[dict]:
        """Execute hybrid search.

        Args:
            query: Search query text.
            db_type: Optional filter by database type.
            filters: Optional field filters (status, owner, type, scope).
            top_k: Number of final results (default: settings.rerank_top_k).
            rerank: Whether to apply cross-encoder reranking.

        Returns:
            List of result dicts with 'text', 'score', 'metadata'.
        """
        final_k = top_k or settings.rerank_top_k
        retrieve_k = settings.search_top_k

        # 1. Encode query
        dense_vec = list(self.dense_model.embed([query]))[0].tolist()
        sparse_vec_raw = list(self.sparse_model.embed([query]))[0]
        sparse_vec = {
            "indices": sparse_vec_raw.indices.tolist(),
            "values": sparse_vec_raw.values.tolist(),
        }

        # 2. Dual retrieval
        dense_hits = self.store.search_dense(
            dense_vec, top_k=retrieve_k, db_type=db_type, filters=filters
        )
        sparse_hits = self.store.search_sparse(
            sparse_vec, top_k=retrieve_k, db_type=db_type, filters=filters
        )

        # 3. RRF fusion
        fused = _rrf_fusion(dense_hits, sparse_hits, k=60)

        # Take top candidates for reranking
        candidates = fused[: retrieve_k]

        if not candidates:
            return []

        # 4. Rerank (optional)
        if rerank and len(candidates) > 1:
            candidates = self._rerank(query, candidates, top_k=final_k)
        else:
            candidates = candidates[:final_k]

        return candidates

    def _rerank(self, query: str, candidates: list[dict], top_k: int) -> list[dict]:
        """Rerank candidates using cross-encoder."""
        texts = [c["text"] for c in candidates]
        scores = list(self.reranker.rerank(query, texts))

        for candidate, score in zip(candidates, scores):
            candidate["rerank_score"] = float(score)

        candidates.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)
        return candidates[:top_k]


def _rrf_fusion(
    dense_hits: list, sparse_hits: list, k: int = 60
) -> list[dict]:
    """Reciprocal Rank Fusion: merge two ranked lists without manual weight tuning.

    RRF score = sum(1 / (k + rank_i)) for each list where the doc appears.
    """
    scores: dict[str, float] = {}
    payloads: dict[str, dict] = {}

    for rank, hit in enumerate(dense_hits):
        chunk_id = hit.payload.get("chunk_id", hit.id)
        scores[chunk_id] = scores.get(chunk_id, 0) + 1.0 / (k + rank + 1)
        payloads[chunk_id] = hit.payload

    for rank, hit in enumerate(sparse_hits):
        chunk_id = hit.payload.get("chunk_id", hit.id)
        scores[chunk_id] = scores.get(chunk_id, 0) + 1.0 / (k + rank + 1)
        payloads[chunk_id] = hit.payload

    # Sort by fused score descending
    sorted_ids = sorted(scores, key=lambda cid: scores[cid], reverse=True)

    results = []
    for cid in sorted_ids:
        payload = payloads[cid]
        results.append({
            "chunk_id": cid,
            "text": payload.get("text", ""),
            "score": scores[cid],
            "metadata": {
                k: v for k, v in payload.items() if k != "text"
            },
        })
    return results
