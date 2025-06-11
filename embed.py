# embed.py — for Bratz GPT

import os
import json
import argparse
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# ✅ Config
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
INDEX_DIR = "bratz_data/index"
DATA_DIR = "bratz_data/data"

# ✅ Create paths if they don't exist
os.makedirs(INDEX_DIR, exist_ok=True)

# ✅ Load model
model = SentenceTransformer(EMBED_MODEL)

# ✅ Chunking helper
def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk.strip())
    return chunks

# ✅ Embed text chunks and store with metadata
all_chunks = []
metadata = []
doc_id = 0

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".txt"):
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            raw_text = f.read()

        chunks = chunk_text(raw_text)
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "doc_id": doc_id,
                "source": filename,
                "text": chunk
            })

        doc_id += 1

# ✅ Create FAISS index
embeddings = model.encode(all_chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# ✅ Save index and metadata
faiss.write_index(index, os.path.join(INDEX_DIR, "bratz_vector_index.faiss"))

with open(os.path.join(INDEX_DIR, "bratz_chunk_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"✅ Indexed {len(all_chunks)} chunks from {doc_id} documents.")