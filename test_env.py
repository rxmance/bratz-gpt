import os
from dotenv import load_dotenv

load_dotenv()

print("🔑 OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10], "...")
print("📁 OPENAI_PROJECT_ID:", os.getenv("OPENAI_PROJECT_ID"))
print("🏢 OPENAI_ORG_ID:", os.getenv("OPENAI_ORG_ID"))