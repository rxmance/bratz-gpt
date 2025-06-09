import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import faiss

# Load environment variables
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID"),
    organization=os.getenv("OPENAI_ORG_ID"),
)

# Load cleaned chunks
with open("fanlabs_data/index/fanlabs_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Filter and clean text chunks
texts = [chunk["content"].strip() for chunk in chunks if chunk.get("content", "").strip()]
if not texts:
    raise ValueError("❌ No valid chunks found to embed.")

# Create embeddings
print(f"🔍 Embedding {len(texts)} chunks using text-embedding-3-small...")
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

# Convert to FAISS-compatible format
vectors = np.array([r.embedding for r in response.data]).astype("float32")
if vectors.shape[0] == 0:
    raise RuntimeError("❌ No vectors returned from OpenAI.")

# Build FAISS index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
os.makedirs("fanlabs_data/index", exist_ok=True)
faiss.write_index(index, "fanlabs_data/index/fanlabs_vector_index.faiss")

# Save metadata
metadata = [{"text": text} for text in texts]
with open("fanlabs_data/index/fanlabs_chunk_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("✅ Embedding + FAISS index created and saved to fanlabs_data/index/")