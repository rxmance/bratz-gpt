import streamlit as st
import openai
import os
import faiss
import json
import numpy as np
import asyncio
import nest_asyncio
nest_asyncio.apply()
from utils.faiss_helpers import load_index_and_metadata
from utils.prompts import build_prompt
from utils.search import search_index

# ✅ Use environment variable for OpenAI key (not st.secrets)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load vector index and metadata
index, metadata = load_index_and_metadata()

# App UI
st.set_page_config(page_title="FanLabs GPT", layout="wide")
st.title("🤖 FanLabs GPT")
st.markdown("Ask me anything based on the book *Fans Have More Friends*.")

# Input
query = st.text_input("Your question:")

# Process
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results)
        with st.spinner("Generating answer..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that uses context from a book to answer questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### Answer")
            st.write(response["choices"][0]["message"]["content"])

            st.markdown("### Sources")
            for i, result in enumerate(results):
                st.markdown(f"**{i+1}.** {result['source']} — {result['text'][:100]}...")
    else:
        st.warning("No relevant context found.")