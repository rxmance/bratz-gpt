import json
import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv

# === Step 1: Load environment variables ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Step 2: Load tagged chunk data ===
with open("bratz_tagged_chunks.json", "r") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]
sources = [chunk["source"] for chunk in chunks]

# === Step 3: Embed using OpenAI API ===
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

print("🔄 Embedding chunks with OpenAI...")
embeddings = [get_embedding(text) for text in texts]
embeddings = np.array(embeddings).astype("float32")

# === Step 4: Build and save FAISS index ===
print("💾 Building FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "bratz_vector_index.faiss")

with open("bratz_chunk_metadata.json", "w") as f:
    json.dump([{"text": t, "source": s} for t, s in zip(texts, sources)], f, indent=2)

print("✅ Done! Files saved:")
print("- bratz_vector_index.faiss")
print("- bratz_chunk_metadata.json")