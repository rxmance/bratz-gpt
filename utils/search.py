import faiss
import numpy as np
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-small"

def embed_query(query: str) -> np.ndarray:
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=[query]
    )
    return np.array(response.data[0].embedding, dtype="float32")

def search_index(query: str, index, metadata: list, top_k: int = 5):
    query_vector = embed_query(query)
    D, I = index.search(np.array([query_vector]), top_k)

    results = []
    for i in I[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results
