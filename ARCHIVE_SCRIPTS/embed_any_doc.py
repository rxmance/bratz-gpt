# embed_any_doc.py

import os
import json
import argparse
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

EMBED_MODEL = "text-embedding-3-small"

def embed_texts(texts):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    return [d.embedding for d in response.data]

def main():
    parser = argparse.ArgumentParser(description="Embed a chunked JSON doc into a FAISS index")
    parser.add_argument("--input", required=True, help="Path to the chunked .json file in output/")
    args = parser.parse_args()

    input_path = args.input
    with open(input_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"🔢 Embedding {len(chunks)} chunks from {input_path}...")

    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts)

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))

    # Save index and metadata
    out_base = os.path.splitext(os.path.basename(input_path))[0].replace("_chunks", "")
    faiss.write_index(index, f"{out_base}_vector_index.faiss")
    with open(f"{out_base}_chunk_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"✅ FAISS index and metadata saved for {out_base}")

if __name__ == "__main__":
    main()
