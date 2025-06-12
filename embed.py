# 💋 Bratz GPT — Custom Chatbot README

Welcome to **Bratz GPT**, your custom-trained chatbot that speaks in the Bratz brand voice and responds in character as Yasmin, Cloe, Jade, Sasha, or Raya. This README walks through everything you need to run, update, and manage your Bratz GPT.

---

## 🚀 Quick Start

### 1. Activate Your Virtual Environment
```bash
cd bratz-gpt
source venv/bin/activate
```

### 2. Embed New Documents (When You Add Data)
Save your `.txt` files into:
```
bratz_data/data/
```

Then run:
```bash
python embed.py
```
> ✅ This creates your updated FAISS vector index and metadata.

---

## 🧠 GPT Logic

- **Embedding model:** `text-embedding-3-small` (via OpenAI)
- **Retrieval:** FAISS
- **System Prompt:** Defined per voice in `utils/prompts.py`
- **Query Processing:** Top 5 relevant chunks
- **Brand & Character voices:** Selected via dropdown in Streamlit UI

---

## 🗂️ Folder Structure
```
bratz-gpt/
├── app.py                      # Main Streamlit app
├── embed.py                   # Embeds data and builds index
├── requirements.txt           # Dependencies
├── bratz_data/
│   ├── data/                  # Upload clean .txt files here
│   └── index/                 # Auto-generated FAISS index & metadata
├── utils/
│   ├── prompts.py             # Core system prompts per voice
│   ├── search.py              # FAISS retrieval logic
│   └── faiss_helpers.py       # Loads index & metadata
└── .env                       # API keys (OpenAI, etc.)
```

---

## 🌐 Deployment (Render)

### Push Changes to GitHub
```bash
git add .
git commit -m "Update Bratz GPT prompts and docs"
git push origin main
```

### Reboot on Render
1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Navigate to `bratz-gpt`
3. Click **Manual Deploy > Clear Cache & Deploy**

> 🔐 Make sure your Render Secrets are set (OpenAI key, org ID, project ID).

---

## 🗣️ Customizing Voices
You can edit system prompts and tone for each Bratz voice here:
```
utils/prompts.py
```
Each character has their own section. Keep the tone punchy, confident, and on-brand.

---

## ✅ To-Do / Nice-to-Have
- [ ] Add logging or basic analytics
- [ ] Add quote-level scoring display in UI
- [ ] Add multi-GPT routing (FanLabs + Bratz)

---

## 💬 Test Prompt Example
> **Prompt:** "What makes Bratz different from other fashion brands today?"
> 
> **Voice:** Jade

---

Let’s keep it bold. Let’s keep it Bratz 💅
