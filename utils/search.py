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
from utils.embedding import get_embedding
import numpy as np

def search_index(query, index, metadata, top_k=5, diversity_threshold=0.9):
    query_vector = np.array(get_embedding(query), dtype=np.float32)
    scores, indices = index.search(np.array([query_vector]), top_k * 2)

    seen_texts = set()
    results = []

    for idx, score in zip(indices[0], scores[0]):
        if idx == -1:
            continue

        item = metadata[idx]
        text = item.get("text", "").strip()

        # Skip overly similar quotes (same or near-identical text)
        if any(text.lower() in seen.lower() or seen.lower() in text.lower() for seen in seen_texts):
            continue

        seen_texts.add(text)
        item["score"] = float(score)
        results.append(item)

        if len(results) >= top_k:
            break

    return results