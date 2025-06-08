# merge_chunks.py

import os
import json

INPUT_DIR = "output"
OUTPUT_FILE = "output/combined_chunks.json"

all_chunks = []

for filename in os.listdir(INPUT_DIR):
    if filename.endswith("_chunks.json"):
        path = os.path.join(INPUT_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
            print(f"✅ Added {len(chunks)} chunks from {filename}")

print(f"\n📦 Total combined chunks: {len(all_chunks)}")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)
print(f"💾 Saved combined chunks to {OUTPUT_FILE}")