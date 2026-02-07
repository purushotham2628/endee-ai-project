"""search.py

Convert a user query into an embedding and call Endee's /api/v1/vector/search
to retrieve the top matches.

Requires:
    pip install requests
"""
import requests
from embed import get_embedding

ENDEE_SEARCH = "http://localhost:8080/api/v1/vector/search"


def search(query: str, top_k: int = 2) -> dict:
    """Search Endee using the embedding for `query`.

    Returns a normalized dictionary containing the raw response and a
    simplified `matches` list with keys: `id`, `score`, `text`, `raw`.
    """
    emb = get_embedding(query)
    payload = {"vector": emb, "top_k": top_k, "include_metadata": True}
    resp = requests.post(ENDEE_SEARCH, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Common response shapes: `matches`, `results`, `data`.
    matches = data.get("matches") or data.get("results") or data.get("data") or []

    extracted = []
    for m in matches:
        # Metadata may live under different keys depending on the server.
        meta = m.get("metadata") or m.get("payload") or {}
        text = meta.get("text") or meta.get("content") or meta.get("original_text")
        score = m.get("score") or m.get("distance") or m.get("similarity")
        extracted.append({"id": m.get("id"), "score": score, "text": text, "raw": m})

    return {"raw": data, "matches": extracted}


if __name__ == "__main__":
    q = "What is DNS used for?"
    print(search(q))
