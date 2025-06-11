### app.py

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
st.set_page_config(page_title="💅 Bratz GPT", layout="wide")
st.title("💅 Bratz GPT")
st.markdown("Let’s bring the Bratz voice to life.")

# 🔀 Brand Voice Selector
brand_voice = st.selectbox(
    "Choose a Bratz brand voice:",
    ["Bratz Brand – High-level creative director assistant"]
)

# 🎭 Bratz Character Tone Selector
character_voice = st.selectbox(
    "Choose a Bratz creative perspective:",
    [
        "Cloe – Dreamy, empathetic, creative",
        "Jade – Edgy, fashion-forward, experimental",
        "Sasha – Strong, driven, musical",
        "Yasmin – Thoughtful, spiritual, poetic",
        "Raya – Bold, funny, grounded"
    ]
)

# ✅ User input
query = st.text_input("What do you want Bratz GPT to help with?")

# ✅ Process query
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results, brand_voice, character_voice)
        with st.spinner("Thinking like a Bratz girl..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": get_system_prompt(brand_voice, character_voice)
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            output = response.choices[0].message.content
            st.markdown("### Answer")
            st.write(output)
    else:
        st.warning("No relevant content found to support this prompt.")