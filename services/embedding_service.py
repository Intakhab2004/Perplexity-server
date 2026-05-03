from typing import List
from google import genai
from helpers.config import settings


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_embedding(texts: List[str]) -> List[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )

    return result.embeddings