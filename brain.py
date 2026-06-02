import os
import json
import ollama

OUTPUT_DIR = "outputs"

def embed_text(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]

def build_embeddings(papers):
    for p in papers:
        text = " ".join([
            " ".join(p.get("summary", [])),
            " ".join(p.get("key_findings", []))
        ])

        p["embedding"] = embed_text(text)

    return papers

import math

def cosine_similarity(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(x*x for x in b))
    return dot / (norm_a * norm_b)

def load_library():
    papers = []

    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".json"):
            path = os.path.join(OUTPUT_DIR, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    data["source_file"] = file
                    papers.append(data)
            except:
                print(f"Skipping broken file: {file}")

    return papers
    
def find_relevant_papers(query, papers, top_k=5):
    query_embedding = embed_text(query)

    scored = []

    for p in papers:
        if "embedding" not in p:
            continue

        score = cosine_similarity(query_embedding, p["embedding"])
        scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [p for _, p in scored[:top_k]]

def ask_llm(query, context):
    prompt = f"""
- Cite sources using (source_file)
    
You are a research assistant.

Answer the question using the provided papers.

QUESTION:
{query}

PAPERS:
{json.dumps(context, indent=2)}

Rules:
- Write a clear, detailed answer
- Synthesize across papers
- Cite sources using (source_file)
- Do NOT output JSON
- Be specific and analytical
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

def main():
    print("Loading literature brain...")

    papers = load_library()
    print(f"Loaded {len(papers)} papers")

    while True:
        query = input("\nAsk your library (or 'exit'): ")

        if query.lower() == "exit":
            break

        relevant = find_relevant_papers(query, papers)

        # keep only useful fields
        relevant = [
            {
                "summary": p.get("summary", []),
                "key_findings": p.get("key_findings", []),
                "source_file": p.get("source_file", "")
            }
            for p in relevant
]

        if not relevant:
            print("No relevant papers found.")
            continue

        answer = ask_llm(query, relevant)
        print("\n" + answer)

if __name__ == "__main__":
    main()    