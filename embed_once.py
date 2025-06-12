# embed_once.py — One-time Bratz embedding script

import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# === Step 1: Load pre-tagged Bratz chunks ===
with open("bratz_tagged_chunks.json", "r") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]
sources = [chunk["source"] for chunk in chunks]

# === Step 2: Generate embeddings ===
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Loaded embedding model")

embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# === Step 3: Create FAISS index ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Step 4: Save FAISS index and metadata ===
faiss.write_index(index, "bratz_vector_index.faiss")

with open("bratz_chunk_metadata.json", "w") as f:
    json.dump([{"text": t, "source": s} for t, s in zip(texts, sources)], f, indent=2)

print("✅ Embedding complete. Files saved:")
print("- bratz_vector_index.faiss")
print("- bratz_chunk_metadata.json")
