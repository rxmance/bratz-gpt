import streamlit as st
import os
import faiss
import json
import numpy as np
import nest_asyncio

from openai import OpenAI
from dotenv import load_dotenv

from utils.faiss_helpers import load_index_and_metadata
from utils.prompts import build_prompt, get_system_prompt
from utils.search import search_index

# ✅ Enable nested loops (required for Streamlit + OpenAI)
nest_asyncio.apply()

# ✅ Load environment variables
load_dotenv()

# ✅ Set up OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID"),
    project=os.getenv("OPENAI_PROJECT_ID"),
)

# ✅ Load FAISS index and chunk metadata
index, metadata = load_index_and_metadata()

# ✅ Streamlit UI setup
st.set_page_config(page_title="FanLabs GPT", layout="wide")
st.title("🤖 FanLabs GPT")
st.markdown("Let’s talk fandom.")
# 🔀 Tone selector
tone = st.selectbox(
    "Choose a voice for FanLabs GPT:",
    ["Strategist", "Provocateur", "Historian"],
    index=0  # Default is now Strategist
)

# ✅ User input
query = st.text_input("Your question:")

# ✅ Process query
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results, tone)
        with st.spinner("Generating answer..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": get_system_prompt(tone)
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### Answer")
            st.write(response.choices[0].message.content)
    else:
        st.warning("No relevant context found.")