import streamlit as st
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from huggingface_hub import login

from utils.openai_client import client
from utils.prompts import base_system_prompt
from utils.faiss_helpers import load_index_and_metadata  # ✅ FIXED

# === Hugging Face Auth ===
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if hf_token:
    login(token=hf_token)
else:
    st.error("❌ Hugging Face token not found in secrets or environment.")
    st.stop()

# === Page Setup ===
st.set_page_config(page_title="FanLabs GPT", layout="wide")
st.title("💬 FanLabs GPT")
st.markdown("Ask a question based on the book *Fans Have More Friends*.")

# === Input box ===
user_query = st.text_input("Ask a question:")

if user_query:
    st.write("⏳ Searching knowledge base...")
    
    try:
        index, metadata = load_index_and_metadata()
    except Exception as e:
        st.error(f"❌ Failed to load index or metadata: {e}")
        st.stop()

    try:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        query_embedding = model.encode([user_query])
    except Exception as e:
        st.error(f"❌ Failed to load or run embedding model: {e}")
        st.stop()

    # === Search index ===
    D, I = index.search(np.array(query_embedding).astype("float32"), k=5)
    retrieved_chunks = [metadata[i]["text"] for i in I[0]]
    context = "\n\n".join(retrieved_chunks)

    # === Build prompt ===
    messages = [
        {"role": "system", "content": base_system_prompt},
        {"role": "user", "content": f"{context}\n\n{user_query}"}
    ]

    # === Get completion ===
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        st.markdown("### ✅ Response")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"❌ OpenAI call failed: {e}")