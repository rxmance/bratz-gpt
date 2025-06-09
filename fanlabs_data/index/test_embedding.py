# test_embedding.py

from utils.embedding import get_embedding

test_text = "Why is fandom a social asset, not just entertainment?"

embedding = get_embedding(test_text)

print(f"✅ Embedding generated. Vector length: {len(embedding)}")
print(f"🔢 First 5 values: {embedding[:5]}")