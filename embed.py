from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np
import os

# === Load chunked data ===
chunk_file = "fanlabs_chunks.json"
if not os.path.exists(chunk_file):
    raise FileNotFoundError(f"❌ Missing input file: {chunk_file}")

with open(chunk_file, "r") as f:
    chunks = json.load(f)

# === Load embedding model ===
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# === Generate embeddings and metadata ===
vectors = []
metadata = []

for i, chunk in enumerate(chunks):
    content = chunk.get("content", "").strip()
    if not content:
        continue  # skip empty chunks

    vector = model.encode(content)
    vectors.append(vector)
    metadata.append({
        "id": i,
        "text": content,
        "source": chunk.get("document_title", "unknown")
    })

# === Convert to FAISS index ===
index = faiss.IndexFlatL2(len(vectors[0]))
index.add(np.array(vectors).astype("float32"))

# === Save index and metadata ===
faiss.write_index(index, "fanlabs_vector_index.faiss")

with open("fanlabs_chunk_metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"✅ Embedded {len(vectors)} chunks")
print("📁 Saved: fanlabs_vector_index.faiss + fanlabs_chunk_metadata.json")