from typing import List
from google import genai
from helpers.config import settings
import time


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def batch_list(data, batch_size = 80):
    for i in range(0, len(data), batch_size):
        yield data[i : i+batch_size]


def generate_embedding(texts: List[str]) -> List[List[float]]:
    all_embeddings = []

    try:
        for batch in batch_list(texts, 80):
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch
            )

            embeddings = [emb.values for emb in result.embeddings]
            all_embeddings.extend(embeddings)
            time.sleep(1)
        
        return all_embeddings
        
    except Exception as e:
        raise Exception(f"Embedding error: {str(e)}")