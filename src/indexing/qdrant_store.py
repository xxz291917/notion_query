"""Qdrant vector store: dual-vector (dense + sparse) write/update/delete."""

import logging
import uuid

from qdrant_client import QdrantClient, models

from src.config import settings

logger = logging.getLogger(__name__)

DENSE_VECTOR_NAME = "dense"
SPARSE_VECTOR_NAME = "sparse"
DENSE_DIM = 1024  # intfloat/multilingual-e5-large


class QdrantStore:
    """Manages a Qdrant collection with dense + sparse vectors."""

    def __init__(self):
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.collection = settings.qdrant_collection

    def ensure_collection(self) -> None:
        """Create collection if it doesn't exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection in collections:
            logger.info(f"Collection '{self.collection}' already exists")
            self._ensure_indexes()
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config={
                DENSE_VECTOR_NAME: models.VectorParams(
                    size=DENSE_DIM,
                    distance=models.Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                SPARSE_VECTOR_NAME: models.SparseVectorParams(
                    modifier=models.Modifier.IDF,
                ),
            },
        )
        # Indexes for filtered search and incremental delete
        self.client.create_payload_index(
            collection_name=self.collection,
            field_name="db_type",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        self.client.create_payload_index(
            collection_name=self.collection,
            field_name="notion_id",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )
        logger.info(f"Created collection '{self.collection}' with dense + sparse vectors")

    def _ensure_indexes(self) -> None:
        """Ensure required payload indexes exist (idempotent)."""
        info = self.client.get_collection(self.collection)
        existing = set(info.payload_schema.keys()) if info.payload_schema else set()
        for field in ("db_type", "notion_id"):
            if field not in existing:
                self.client.create_payload_index(
                    collection_name=self.collection,
                    field_name=field,
                    field_schema=models.PayloadSchemaType.KEYWORD,
                )
                logger.info(f"Created index on '{field}'")

    def upsert_chunks(
        self,
        chunks: list[dict],
        dense_vectors: list[list[float]],
        sparse_vectors: list[dict],
    ) -> None:
        """Upsert chunks with their embeddings into Qdrant."""
        points = []
        for chunk, dense_vec, sparse_vec in zip(chunks, dense_vectors, sparse_vectors):
            point_id = _deterministic_uuid(chunk["chunk_id"])
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector={
                        DENSE_VECTOR_NAME: dense_vec,
                        SPARSE_VECTOR_NAME: models.SparseVector(
                            indices=sparse_vec["indices"],
                            values=sparse_vec["values"],
                        ),
                    },
                    payload={
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"],
                        **chunk["metadata"],
                    },
                )
            )

        self.client.upsert(collection_name=self.collection, points=points)
        logger.info(f"Upserted {len(points)} points")

    def delete_by_notion_id(self, notion_id: str) -> None:
        """Delete all chunks belonging to a Notion page."""
        self.client.delete(
            collection_name=self.collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="notion_id",
                            match=models.MatchValue(value=notion_id),
                        )
                    ]
                )
            ),
        )
        logger.info(f"Deleted chunks for notion_id={notion_id}")

    def search_dense(
        self,
        vector: list[float],
        top_k: int = 20,
        db_type: str | None = None,
    ) -> list[models.ScoredPoint]:
        """Search by dense vector with optional db_type filter."""
        query_filter = _build_filter(db_type)
        return self.client.query_points(
            collection_name=self.collection,
            query=vector,
            using=DENSE_VECTOR_NAME,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        ).points

    def search_sparse(
        self,
        sparse_vector: dict,
        top_k: int = 20,
        db_type: str | None = None,
    ) -> list[models.ScoredPoint]:
        """Search by sparse vector with optional db_type filter."""
        query_filter = _build_filter(db_type)
        return self.client.query_points(
            collection_name=self.collection,
            query=models.SparseVector(
                indices=sparse_vector["indices"],
                values=sparse_vector["values"],
            ),
            using=SPARSE_VECTOR_NAME,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        ).points

    def count(self) -> int:
        return self.client.count(collection_name=self.collection).count


def _build_filter(db_type: str | None) -> models.Filter | None:
    if not db_type:
        return None
    return models.Filter(
        must=[
            models.FieldCondition(
                key="db_type", match=models.MatchValue(value=db_type)
            )
        ]
    )


def _deterministic_uuid(key: str) -> str:
    """Generate a deterministic UUID from a string key for idempotent upserts."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, key))
