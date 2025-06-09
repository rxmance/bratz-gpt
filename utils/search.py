from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")  # same as embed.py

def search_index(query, index, metadata, top_k=5):
    query_vector = model.encode([query])[0].astype(np.float32)
    scores, indices = index.search(np.array([query_vector]), top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(metadata):
            chunk = metadata[idx]
            results.append({
                "score": float(score),
                "text": chunk.get("text") or chunk.get("content"),
                "title": chunk.get("document_title", "Unknown"),
                "section": chunk.get("section", ""),
            })
    return results