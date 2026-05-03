from typing import List, Dict
from helpers.config import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from services.embedding_service import generate_embedding

client = QdrantClient(url=settings.QDRANT_URL)


def store_embeddings(chunks: List[Dict]):
    # Creating collection for vector_db
    client.create_collection(
        collection_name="content_collection",
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

    texts = [chunk.get("text", "") for chunk in chunks]
    embeddings = generate_embedding(texts)

    points = []
    for i, chunk in enumerate(chunks):
        points.append({
            "id": i,
            "embedding": embeddings[i].values,
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
    print("Vector store info: ", info)


# TODO: Check this pipeline and create a function for similarity search

