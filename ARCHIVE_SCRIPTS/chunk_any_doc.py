# chunk_any_doc.py

import os
import json
import argparse
import re
from typing import List, Dict
import tiktoken

ENCODING = "cl100k_base"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def clean_text(text: str) -> str:
    text = re.sub(r"\n{2,}", "\n", text)
    text = re.sub(r"Page \d+ of \d+", "", text)
    text = text.replace("\xa0", " ")
    return text.strip()

def chunk_text(text: str, chunk_size: int, overlap: int, source: str, filename: str) -> List[Dict]:
    enc = tiktoken.get_encoding(ENCODING)
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = []
    current_tokens = 0
    chunk_index = 0

    for sentence in sentences:
        token_count = len(enc.encode(sentence))
        if current_tokens + token_count > chunk_size:
            if current_chunk:
                full_text = " ".join(current_chunk)
                chunks.append({
                    "text": full_text,
                    "chunk_index": chunk_index,
                    "source": source,
                    "filename": filename
                })
                chunk_index += 1
                overlap_text = " ".join(current_chunk)[-overlap * 4:]
                current_chunk = [overlap_text] if overlap_text else []
                current_tokens = len(enc.encode(" ".join(current_chunk)))
        current_chunk.append(sentence)
        current_tokens += token_count

    if current_chunk:
        chunks.append({
            "text": " ".join(current_chunk),
            "chunk_index": chunk_index,
            "source": source,
            "filename": filename
        })

    return chunks

def save_chunks(chunks: List[Dict], output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Clean and chunk any .txt doc")
    parser.add_argument("--input", required=True, help="Path to input .txt file (in data/)")
    parser.add_argument("--source", required=True, help="Source name to tag the chunks (e.g., fans_book, research_memo)")
    args = parser.parse_args()

    input_path = args.input
    filename = os.path.basename(input_path)
    source_name = args.source
    output_path = f"output/{os.path.splitext(filename)[0]}_chunks.json"

    print(f"🔍 Loading {filename}...")
    raw_text = load_text(input_path)

    print("🧼 Cleaning text...")
    cleaned = clean_text(raw_text)

    print("✂️ Chunking text...")
    chunks = chunk_text(cleaned, CHUNK_SIZE, CHUNK_OVERLAP, source_name, filename)

    print(f"✅ Created {len(chunks)} chunks")
    save_chunks(chunks, output_path)
    print(f"💾 Saved to {output_path}")

if __name__ == "__main__":
    main()