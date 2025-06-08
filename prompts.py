def build_prompt(context, docs, persona):
    knowledge = "\n".join(docs)
    return f"""
You are an assistant that generates believable excuses for a {persona}.
Context: {context}
Use the following evidence if helpful:\n{knowledge}
Generate a natural-sounding, proof-backed excuse:
"""
