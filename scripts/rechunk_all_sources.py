import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from docx import Document
from utils.chunking import chunk_text

# Map of filenames to output names
docs = {
    "dirty data/_BOOK-FHMF_FINAL_EXPORTED-1.docx": "fans_have_more_friends_book",
    "dirty data/_ReDforFox_Sports is Belonging_05062025.docx": "red_sports_belonging",
    "dirty data/Fandom as a Cure to Loneliness Epidemic with Ben Valenta of FOX Sports  Play Equity Summit 2024.docx": "ben_talk_fandom_lonliness",
    "dirty data/Give the gift of fandom this holiday season v2.docx": "gift_of_fandom",
}

def extract_text(path):
    doc = Document(path)
    return "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def main():
    os.makedirs("output", exist_ok=True)
    for path, name in docs.items():
        print(f"Processing: {path}")
        text = extract_text(path)
        chunks = chunk_text(text)
        print(f"→ {len(chunks)} chunks")
        output_data = [{
            "text": c,
            "source": name.replace("_", " ").title(),
            "title": name,
            "document_title": name.replace("_", " ").title()
        } for c in chunks]
        with open(f"output/{name}_chunks.json", "w") as f:
            json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()