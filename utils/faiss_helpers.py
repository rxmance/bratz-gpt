import faiss
import json

def load_index_and_metadata():
    index = faiss.read_index("bratz_vector_index.faiss")
    with open("bratz_chunk_metadata.json", "r") as f:
        metadata = json.load(f)
    return index, metadata