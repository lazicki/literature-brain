import os
import json
import ollama

OUTPUT_DIR = "outputs"

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
    
def find_relevant_papers(query, papers):
    query_words = query.lower().split()
    scored = []

    for p in papers:
        text = json.dumps(p).lower()
        score = sum(word in text for word in query_words)

        if score > 0:
            scored.append((score, p))

    # sort by relevance
    scored.sort(reverse=True, key=lambda x: x[0])

    return [p for _, p in scored[:5]]

def ask_llm(query, context):
    prompt = f"""
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
            for p in relevant[:max_papers]
]

        if not relevant:
            print("No relevant papers found.")
            continue

        answer = ask_llm(query, relevant)
        print("\n" + answer)

if __name__ == "__main__":
    main()    