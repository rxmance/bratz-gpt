import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

# Load .env vars
load_dotenv()
client = OpenAI()

# Load chunks
with open("cleaned_chunks.json", "r") as f:
    chunks = json.load(f)

# Filter & clean
texts = [chunk["content"].strip() for chunk in chunks if chunk.get("content", "").strip()]

# Embed
print(f"Embedding {len(texts)} chunks...")

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

# Convert to numpy
vectors = np.array([r.embedding for r in response.data]).astype("float32")

if len(vectors) == 0:
    raise RuntimeError("❌ No vectors created. Check your input data.")

# Save index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
faiss.write_index(index, "fanlabs_vector_index.faiss")

# Save metadata
metadata = [{"text": text} for text in texts]
with open("fanlabs_chunk_metadata.json", "w") as f:
    json.dump(metadata, f)

print("✅ Embedding + FAISS index complete")