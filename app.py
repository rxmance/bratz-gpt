import streamlit as st
import os
import faiss
import json
import numpy as np
import nest_asyncio
from openai import OpenAI
from utils.faiss_helpers import load_index_and_metadata
from utils.prompts import build_prompt
from utils.search import search_index

nest_asyncio.apply()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Load vector index and metadata
index, metadata = load_index_and_metadata()

# App UI
st.set_page_config(page_title="FanLabs GPT", layout="wide")
st.title("🤖 FanLabs GPT")
st.markdown("Let's talk fandom")

# Input
query = st.text_input("Your question:")

# Process
if query:
    results = search_index(query, index, metadata, top_k=5)
    if results:
        prompt = build_prompt(query, results)
        with st.spinner("Generating answer..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that uses context from a book to answer questions."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.markdown("### Answer")
            st.write(response.choices[0].message.content)
    else:
        st.warning("No relevant context found.")
