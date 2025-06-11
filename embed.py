# embed.py — Bratz GPT (OpenAI Version to match FanLabs)

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

# ✅ Load environment variables
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID"),
)

# ✅ Config
DATA_DIR = "bratz_data/data"
INDEX_DIR = "bratz_data/index"
os.makedirs(INDEX_DIR, exist_ok=True)

# ✅ Load and clean text files
all_chunks = []
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".txt"):
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            raw = f.read().strip()
            if raw:
                all_chunks.append({"source": filename, "text": raw})

# ✅ Split into chunks (simple greedy split)
def chunk_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk.strip())
    return chunks

chunked_data = []
for doc in all_chunks:
    chunks = chunk_text(doc["text"])
    for chunk in chunks:
        chunked_data.append({"text": chunk, "source": doc["source"]})

texts = [chunk["text"] for chunk in chunked_data]
if not texts:
    raise ValueError("❌ No valid text chunks found to embed.")

# ✅ Embed with OpenAI
print(f"🔍 Embedding {len(texts)} chunks using text-embedding-3-small...")
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

# ✅ Build FAISS index
vectors = np.array([r.embedding for r in response.data]).astype("float32")
if vectors.shape[0] == 0:
    raise RuntimeError("❌ No vectors returned from OpenAI.")

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
faiss.write_index(index, os.path.join(INDEX_DIR, "bratz_vector_index.faiss"))

# ✅ Save metadata
with open(os.path.join(INDEX_DIR, "bratz_chunk_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(chunked_data, f, ensure_ascii=False, indent=2)

print(f"✅ Indexed {len(texts)} chunks from {len(all_chunks)} documents.")
