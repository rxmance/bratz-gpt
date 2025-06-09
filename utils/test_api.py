from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)

import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer

print("✅ Starting basic environment test...")

# 🔍 Debug print your env variables
print("🔍 OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
print("🔍 OPENAI_PROJECT_ID:", os.environ.get("OPENAI_PROJECT_ID"))
print("🔍 OPENAI_ORG_ID:", os.environ.get("OPENAI_ORG_ID"))

# Test OpenAI
try:
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        project=os.environ.get("OPENAI_PROJECT_ID"),
        organization=os.environ.get("OPENAI_ORG_ID")
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is 2 + 2?"}]
    )
    print("✅ OpenAI test passed:", response.choices[0].message.content)
except Exception as e:
    print("❌ OpenAI test failed:", e)

# Test HuggingFace
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode("Hello world!")
    print("✅ HuggingFace embedding model test passed.")
except Exception as e:
    print("❌ HuggingFace test failed:", e)