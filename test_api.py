# test_api.py
import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer

print("✅ Starting basic environment test...")

# Test OpenAI
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is 2 + 2?"}]
    )
    print("✅ OpenAI test passed:", response.choices[0].message.content)
except Exception as e:
    print("❌ OpenAI test failed:", e)

# Test HuggingFace embedding model
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode("Hello world!")
    print("✅ HuggingFace embedding model test passed.")
except Exception as e:
    print("❌ HuggingFace test failed:", e)