import re

def chunk_text(text, max_tokens=400):
    # Simple tokenizer: counts words as a proxy for tokens
    def tokenize(s):
        return s.split()

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    current_chunk = []

    for para in paragraphs:
        if sum(len(tokenize(p)) for p in current_chunk + [para]) <= max_tokens:
            current_chunk.append(para)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [para]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks