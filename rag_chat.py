"""rag_chat.py

Simple semantic search CLI demo using Endee vector database.

This script prompts the user for a question, calls `search()` from
`search.py`, and prints the top matches with score and stored text.

No OpenAI or LLM dependencies are used.
"""
from search import search


def main():
    print("=" * 60)
    print("SEMANTIC SEARCH DEMO")
    print("=" * 60)
    print("This demo asks for a user question, searches the Endee index, and prints top matches.")

    try:
        query = input("\nEnter your question: ")
    except KeyboardInterrupt:
        print("\nExiting.")
        return

    print("\nConverting query to embedding and searching...")
    result = search(query, top_k=5)

    if not result.get("success"):
        print("Search failed:", result.get("error"))
        return

    matches = result.get("results", [])
    if not matches:
        print("No matches found.")
        return

    print(f"\nTop {len(matches)} matches:")
    for i, m in enumerate(matches, 1):
        print(f"  {i}. ID: {m['id']}, Score: {m['similarity']:.4f}")
        print(f"     Text: {m.get('text','N/A')}\n")


if __name__ == "__main__":
    main()
