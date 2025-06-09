import json

# Path to your existing combined chunks file
input_path = "output/combined_chunks.json"
output_path = "output/combined_chunks_tagged.json"

# Manually define tags based on known source filenames
tag_map = {
    "gift_of_fandom": {
        "theme": ["connection", "community", "loneliness"],
        "type": "memo",
        "author": "FanLabs"
    },
    "fans_have_more_friends_book": {
        "theme": ["identity", "sports", "belonging"],
        "type": "book",
        "author": "Ben"
    },
    "red_sports_belonging": {
        "theme": ["belonging", "team loyalty", "ritual"],
        "type": "memo",
        "author": "FanLabs"
    },
    "ben_talk_fandom_lonliness": {
        "theme": ["loneliness", "youth", "sports"],
        "type": "talk",
        "author": "Ben"
    }
}

# Load original chunks
with open(input_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Apply tags
for chunk in chunks:
    source = chunk.get("source", "")
    tags = tag_map.get(source, {})
    chunk.update(tags)

# Save new tagged version
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"✅ Tagged and saved to {output_path}")
