import streamlit as st
import os
import faiss
import json
import numpy as np
import nest_asyncio
import re

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
st.set_page_config(page_title="Bratz GPT", layout="wide")
st.title("💋 Bratz GPT")
st.markdown("What’s the vibe? Let’s get into it.")

# 🔀 Voice selector — single dropdown with clean labels
voice = st.selectbox(
    "Choose a Bratz voice:",
    ["Bratz Brand", "Cloe", "Jade", "Sasha", "Yasmin", "Raya"],
    index=0
)

# ✅ User input
query = st.text_input("Your question:")

# ✅ Process query
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results, voice, voice)
        with st.spinner("Thinking like a Bratz queen..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": get_system_prompt(voice, voice)
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            raw_output = response.choices[0].message.content
            st.markdown("### Answer")
            st.write(raw_output)
    else:
        st.warning("No relevant context found.")