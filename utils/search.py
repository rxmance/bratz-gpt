import faiss
import numpy as np
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Ensure .env loads when running locally
load_dotenv(dotenv_path=".env", override=True)

# Initialize OpenAI client with all required fields for project-scoped key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    project=os.environ.get("OPENAI_PROJECT_ID"),
    organization=os.environ.get("OPENAI_ORG_ID")
)

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