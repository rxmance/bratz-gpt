import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import numpy as np
import faiss
from utils.embedding import get_embedding

# Load chunks from output/combined_chunks.json
with open("output/combined_chunks.json", "r") as f:
    chunks = json.load(f)

# Get text chunks
texts = [c["text"] for c in chunks]
print(f"Embedding {len(texts)} chunks...")

# Generate embeddings
embeddings = [get_embedding(t) for t in texts]
embedding_matrix = np.array(embeddings).astype("float32")

# Create FAISS index
index = faiss.IndexFlatL2(embedding_matrix.shape[1])
index.add(embedding_matrix)

# Save index
os.makedirs("fanlabs_data/index", exist_ok=True)
faiss.write_index(index, "fanlabs_data/index/fanlabs_vector_index.faiss")
print("✅ Saved FAISS index to fanlabs_vector_index.faiss")

# Save metadata
with open("fanlabs_data/index/fanlabs_chunk_metadata.json", "w") as f:
    json.dump(chunks, f, indent=2)
print("✅ Saved metadata to fanlabs_chunk_metadata.json")