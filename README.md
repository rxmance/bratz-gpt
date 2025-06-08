# FanLabs GPT

A custom GPT-powered app that uses Retrieval-Augmented Generation (RAG) to answer questions based on the book *Fans Have More Friends*.

## How it works

- Uses FAISS to store and search embedded chunks of the book
- Retrieves top-matching content for a user’s question
- Builds a prompt and sends it to OpenAI’s Chat API
- Hosted on Render using Streamlit

## Deployment (on Render)

1. Set these Environment Variables:
   - `OPENAI_API_KEY` — your OpenAI key
   - `HUGGINGFACE_TOKEN` — your Hugging Face token
2. Use this Start Command:
   ```bash
   streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
## Dependencies

All required libraries are listed in `requirements.txt`.

## Folder Structure
```
fanlabs-gpt-fresh/
├── app.py
├── embed.py
├── fanlabs_chunk_metadata.json
├── fanlabs_vector_index.faiss
├── requirements.txt
├── README.md
├── utils/
│ ├── faiss_helpers.py
│ ├── prompts.py
│ └── search.py
```