import numpy as np
from utils.embedding import get_embedding

# ✅ 1. Combined scoring function (above search_index)
def combined_score(chunk, alpha=1.0, beta=0.0):
    """
    Returns a relevance score for sorting chunks.
    Lower scores are better.
    """
    faiss_score = chunk["score"]
    meta_boost = 0  # Add weighting logic later if desired
    return alpha * faiss_score + beta * meta_boost


# ✅ 2. Your actual search_index function
def search_index(query, index, metadata, top_k=5):
    query_embedding = np.array([get_embedding(query)]).astype("float32")
    scores, indices = index.search(query_embedding, top_k * 4)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        score = scores[0][i]
        entry = metadata[idx]
        entry["score"] = score
        results.append(entry)

    # ✅ Sort by combined score (lower = better)
    top_chunks = sorted(results, key=combined_score)[:top_k]

    # 🔍 Optional: debug print of top chunk scores
    for i, chunk in enumerate(top_chunks):
        print(f"#{i+1}: score={chunk['score']:.4f} | text={chunk['text'][:60]}...")

    return top_chunks