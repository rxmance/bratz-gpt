import streamlit as st
import os
import faiss
import json
import numpy as np
import nest_asyncio
from openai import OpenAI  # ✅ Correct v1.x import

from dotenv import load_dotenv
from utils.faiss_helpers import load_index_and_metadata
from utils.prompts import build_prompt
from utils.search import search_index

# ✅ Enable nested event loops (for Streamlit + async)
nest_asyncio.apply()

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

# ✅ Load FAISS index and metadata
index, metadata = load_index_and_metadata()

# ✅ Streamlit UI setup
st.set_page_config(page_title="FanLabs GPT", layout="wide")
st.title("🤖 FanLabs GPT")
st.markdown("Let’s talk fandom.")

# ✅ Input from user
query = st.text_input("Your question:")

# ✅ Process query
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results)
        with st.spinner("Generating answer..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are FanLabs GPT, a highly intelligent cultural strategist trained on the Fans Have More Friends project. You blend data, theory, and narrative to analyze the role of fandom in society. You challenge surface-level takes, speak with conviction, and always tie insights back to belonging, social capital, and the cultural power of sports. You can respond to op-eds, strategy prompts, or abstract questions, always bringing a FanLabs lens to the topic. You are not generic — you are smart, strategic, and unafraid to make bold claims when supported by research."""
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### Answer")
            st.write(response.choices[0].message.content)
    else:
        st.warning("No relevant context found.")