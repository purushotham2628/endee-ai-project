"""rag_chat.py

Simple RAG (Retrieval-Augmented Generation) example:
  1. Embed user query using sentence-transformers
  2. Search Endee for similar vectors + metadata
  3. Extract context from retrieved metadata
  4. Call OpenAI to answer based ONLY on that context

Requirements:
    pip install openai requests sentence-transformers

Set environment variable: OPENAI_API_KEY=sk-...
"""
import os
from openai import OpenAI
from search import search

# Initialize OpenAI client - reads OPENAI_API_KEY from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def answer_with_rag(question: str) -> str:
    """
    Answer a question using RAG: retrieve context from Endee, then ask OpenAI.
    
    Args:
        question: User question to answer
    
    Returns:
        Answer from OpenAI based on retrieved context
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not set. Please set: export OPENAI_API_KEY=sk-..."
        )
    
    print(f"Question: {question}\n")
    
    # Step 1: Search Endee for relevant vectors
    print("[1] Searching for relevant context...")
    search_result = search(question, top_k=2)
    
    if not search_result.get("success"):
        print(f"Search failed: {search_result.get('error')}")
        return None
    
    # Step 2: Extract context from search results
    results = search_result.get("results", [])
    context_pieces = []
    
    print(f"[2] Found {len(results)} matching vectors.")
    for i, result in enumerate(results, 1):
        meta = result.get("meta", {})
        text = meta.get("text")
        if text:
            context_pieces.append(text)
            print(f"    [{i}] {text[:60]}...")
    
    context = "\n\n".join(context_pieces) if context_pieces else "(no context found)"
    
    # Step 3: Build prompt with context-only instruction
    print(f"\n[3] Calling OpenAI gpt-3.5-turbo...")
    
    system_prompt = (
        "You are a helpful assistant. Answer the user's question using ONLY "
        "the provided context. If the answer is not in the context, say: "
        "'I don't have that information in the provided context.'"
    )
    
    user_prompt = (
        f"Context information:\n"
        f"---\n"
        f"{context}\n"
        f"---\n\n"
        f"Question: {question}\n\n"
        f"Answer based ONLY on the context above:"
    )
    
    try:
        # Call OpenAI ChatCompletion (using new SDK v1.0+)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.0,  # Deterministic answers
        )
        
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None


if __name__ == "__main__":
    print("="*60)
    print("RAG CHAT DEMO")
    print("="*60)
    print()
    
    example_question = "What is the purpose of DNS?"
    
    answer = answer_with_rag(example_question)
    if answer:
        print(f"\n[Answer]")
        print(f"{answer}")
    else:
        print("\nWarning: RAG chat failed. Make sure:")
        print("  1. Index 'notes_index' exists (run create_index.py)")
        print("  2. Vectors are stored (run store_vectors.py)")
        print("  3. OPENAI_API_KEY environment variable is set and valid")
