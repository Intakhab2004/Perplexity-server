from typing import List, Dict
from helpers.config import settings
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from services.embedding_service import generate_embedding


client = QdrantClient(url=settings.QDRANT_URL)


def store_embeddings(chunks: List[Dict]):
    # Generating embeddings
    unique_chunks = {}
    for chunk in chunks:
        text = chunk.get("text", "").strip()

        if text and text not in unique_chunks:
            unique_chunks[text] = chunk
    
    unique_chunks = list(unique_chunks.values())

    texts = [c["text"] for c in unique_chunks]
    embeddings = generate_embedding(texts)

    # Creating collection for vector_db if not exists
    embedding_dimension = len(embeddings[0])
    if not client.collection_exists("content_collection"):
        client.create_collection(
            collection_name="content_collection",
            vectors_config=VectorParams(
                size=embedding_dimension,
                distance=Distance.COSINE
            )
        )


    points = []
    for chunk, embedding in zip(unique_chunks, embeddings):
        points.append({
            "id": str(uuid.uuid4()),
            "vector": embedding,
            "payload": {
                "text": chunk["text"],
                "source": chunk["source"],
                "title": chunk["title"],
                "question": chunk["question"]
            }
        })
    
    info = client.upsert(
        collection_name="content_collection",
        points=points
    )
    return info.status


def search_similar(query: str, top_k: int = 5):
    query_embedding = generate_embedding([query])[0]

    top_k = min(top_k, 5)
    results = client.query_points(
        collection_name="content_collection",
        query=query_embedding,
        limit=top_k
    ).points

    formatted_result = [
        {
            "text": res.payload.get("text") if res.payload else None,
            "source": res.payload.get("source") if res.payload else None,
            "title": res.payload.get("title") if res.payload else None,
            "score": res.score
        }
        for res in results
    ]

    return formatted_result