import os
from dotenv import load_dotenv
from uuid import uuid4
from typing import Optional

from qdrant_client import QdrantClient, models
from ai.rag.tools.embeddings.embedder import Embedder
from ai.rag.tools.embeddings.milvus_store import init_collection
from ai.rag.tools.embeddings.extractors import (
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
)
from ai.rag.tools.embeddings.chunker import chunk_text

load_dotenv()


# ========= GLOBAL RAG (MILVUS) ========= #
def retrieve_context_milvus(query: str, top_k: int = 3):
    collection = init_collection()
    embedder = Embedder()

    query_emb = embedder.embed(query)

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    results = collection.search(
        data=[query_emb],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text", "filename", "timestamp"]
    )

    return "\n\n".join(hit.entity.get("text") for hit in results[0])


# ========= LOCAL TEMPORARY RAG (QDRANT) ========= #
def _extract_text(file_path: str):
    ext = file_path.lower().split(".")[-1]

    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "docx":
        return extract_text_from_docx(file_path)
    elif ext == "txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def retrieve_context_file(query: str, file_path: str, limit: int = 3):
    embedder = Embedder()

    # 1) Extract text
    text = _extract_text(file_path)

    # 2) Chunk text
    chunks = chunk_text(text)

    # 3) Create temporary in-memory vector DB
    qdrant = QdrantClient(location=":memory:")
    coll_name = uuid4().hex

    qdrant.create_collection(
        collection_name=coll_name,
        vectors_config=models.VectorParams(
            size=1024,  # Qwen3 embedding dimension
            distance=models.Distance.COSINE,
        )
    )

    qdrant.upload_points(
        collection_name=coll_name,
        points=[
            models.PointStruct(
                id=i,
                vector=embedder.embed(c),
                payload={"text": c}
            )
            for i, c in enumerate(chunks)
        ]
    )

    # 4) Search
    query_emb = embedder.embed(query)

    result = qdrant.query_points(
        collection_name=coll_name,
        query=query_emb,
        limit=limit
    ).points

    # 5) Cleanup
    qdrant.delete_collection(collection_name=coll_name)

    return "\n\n".join(r.payload["text"] for r in result)


# ========= RAG ROUTER ========= #
def retrieve_context(query: str, file_path: Optional[str] = None):
    """
    Jika file_path diberikan → gunakan Temporary Qdrant (Local RAG).
    Jika tidak → gunakan Milvus (Global RAG).
    """
    if file_path:
        return retrieve_context_file(query, file_path)
    return retrieve_context_milvus(query)
