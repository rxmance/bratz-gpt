import faiss
import numpy as np
import openai
import os
import json

# Make sure the OpenAI API key is loaded
openai.api_key = os.environ.get("OPENAI_API_KEY")

EMBED_MODEL = "text-embedding-3-small"

def embed_query(query: str) -> np.ndarray:
    response = openai.Embedding.create(
        model=EMBED_MODEL,
        input=[query]
    )
    return np.array(response["data"][0]["embedding"], dtype="float32")

def search_index(query: str, index, metadata: list, top_k: int = 5):
    query_vector = embed_query(query)
    D, I = index.search(np.array([query_vector]), top_k)

    results = []
    for i in I[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results