import numpy as np
from utils.embedding import get_embedding

def search_index(query, index, metadata, top_k=5):
    query_vector = np.array([get_embedding(query)]).astype("float32")
    scores, indices = index.search(query_vector, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1:
            continue
        score = scores[0][i]
        entry = metadata[idx]
        entry["score"] = score
        results.append(entry)

    # Sort results by score DESC (most relevant first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results