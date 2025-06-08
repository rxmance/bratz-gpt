import faiss
import json
import numpy as np

def load_index_and_metadata(index_path="combined_vector_index.faiss", metadata_path="combined_chunk_metadata.json"):
    try:
        index = faiss.read_index(index_path)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load FAISS index: {e}")

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load metadata: {e}")

    return index, metadata