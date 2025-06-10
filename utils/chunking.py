import re

def chunk_text(text, max_chars=700, min_chars=350):
    """
    Splits text into chunks based on sentence boundaries.
    Attempts to balance chunk length between min_chars and max_chars.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current += sentence + " "
        else:
            if len(current.strip()) >= min_chars:
                chunks.append(current.strip())
                current = sentence + " "
            else:
                current += sentence + " "

    if current.strip():
        chunks.append(current.strip())

    return chunks