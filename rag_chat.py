"""rag_chat.py

Simple Retrieval-Augmented Generation (RAG) example using a local Endee
vector DB for retrieval and OpenAI for generation. The generator is asked
to answer using ONLY the retrieved context.

Requirements:
    pip install openai requests sentence-transformers

Set the `OPENAI_API_KEY` environment variable before running.
"""
import os
import openai
from search import search

openai.api_key = os.getenv("OPENAI_API_KEY")


def answer_with_rag(query: str) -> str:
    """Retrieve context for `query` and ask OpenAI to answer using only it.

    The function will:
    - call `search(query)` to get the top matches from Endee
    - combine the retrieved `metadata.text` fields into a context block
    - call OpenAI ChatCompletion with an instruction to use only that context
    """
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")

    # Retrieve context from local vector DB
    search_res = search(query, top_k=2)
    matches = search_res.get("matches", [])

    # Collect available texts from matches (skip if missing)
    context_texts = [m["text"] for m in matches if m.get("text")]
    context = "\n\n---\n\n".join(context_texts) if context_texts else ""

    system = (
        "You are a helpful assistant. Answer the user's question using ONLY the provided context. "
        "If the answer is not present in the context, reply: 'I don't know based on the provided context.'"
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer concisely based ONLY on the Context above."

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=512,
        temperature=0.0,
    )

    return resp["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    # Example question demonstrating the flow. Ensure your Endee instance
    # has been populated (run store_vectors.py) and `OPENAI_API_KEY` is set.
    example_q = "What is the purpose of DNS?"
    print("Question:", example_q)
    try:
        print("Answer:", answer_with_rag(example_q))
    except Exception as e:
        print("Error running RAG chat:", e)
