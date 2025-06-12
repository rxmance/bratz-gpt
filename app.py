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
from utils.prompts import build_prompt, get_character_prompt, get_brand_prompt
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

# 🔀 Mode and voice selection
mode = st.radio("Choose your vibe:", ["Talk to a Bratz Character", "Use Bratz Brand Voice"])
selected_voice = None

if mode == "Talk to a Bratz Character":
    selected_voice = st.selectbox("Choose a Bratz character:", ["Cloe", "Jade", "Sasha", "Yasmin", "Raya"])
    system_prompt = get_character_prompt(selected_voice)
else:
    system_prompt = get_brand_prompt()

# ✅ User input
query = st.text_input("Your question:")

# ✅ Helper to filter quotes by character
def filter_by_character(results, character):
    return [r for r in results if r.get("source", "").lower() == character.lower()]

# ✅ Optional: Voice formatting on final response
def apply_voice_formatting(text, character):
    if character == "Cloe":
        return text.replace(".", "✨.").replace("!", "!!! 💖")
    elif character == "Sasha":
        return text + " 💅"
    elif character == "Yasmin":
        return f"🌿 {text} 🌿"
    elif character == "Jade":
        return f"⚡ {text} ⚡"
    elif character == "Raya":
        return f"💬 Real talk: {text}"
    return text

# ✅ Process query
if query:
    results = search_index(query, index, metadata, top_k=5)

    if results:
        if mode == "Talk to a Bratz Character":
            filtered_results = filter_by_character(results, selected_voice)
            if not filtered_results:
                prompt = f"User question: {query}\n\nAnswer like {selected_voice} from Bratz."
            else:
                prompt = build_prompt(query, filtered_results, "Bratz Brand", selected_voice)
        else:
            prompt = build_prompt(query, results, "Bratz Brand", "Bratz Brand")
    else:
        st.info("No relevant context found — answering from pure Bratz vibe.")
        prompt = f"User question: {query}\n\nAnswer like {selected_voice or 'the Bratz brand'} from Bratz."

    with st.spinner("Thinking like a Bratz queen..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        raw_output = response.choices[0].message.content
        final_output = apply_voice_formatting(raw_output, selected_voice) if selected_voice else raw_output
        st.markdown("### Answer")
        st.write(final_output)
