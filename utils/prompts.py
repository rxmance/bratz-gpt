def build_prompt(query, results, tone):
    base_prompt = get_system_prompt(tone)

    formatted_quotes = []
    for i, item in enumerate(results, 1):
        score = item.get("score", 0)
        title = item.get("document_title") or item.get("title", "Unknown Source")
        text = item.get("text", "").strip().replace("\n", " ")
        formatted_quotes.append(f"""
**[{i}] {title}**  
*Relevance Score: {score:.2f}*  
> {text}
""".strip())

    formatted_context = "\n\n".join(formatted_quotes)

    prompt = f"""{base_prompt}

User question:
{query}

Relevant context (higher score = more relevant):
{formatted_context}

Instructions:
Use the most relevant quotes to anchor your answer. Weave in supporting ones if useful. When relevant, include the *document title* in your phrasing for clarity and credibility. Be decisive, strategic, and clear.

Answer:"""

    return prompt