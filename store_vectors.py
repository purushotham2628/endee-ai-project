"""store_vectors.py

Stores a few sample networking sentences into the local Endee vector DB.

Requires:
    pip install requests

This script will POST to http://localhost:8080/api/v1/vector/upsert
using a simple JSON body containing the vector values and metadata.
"""
import uuid
import requests
from embed import get_embedding

ENDEE_UPSERT = "http://localhost:8080/api/v1/vector/upsert"

SENTENCES = [
    "A subnet divides a network into smaller, more manageable pieces.",
    "TCP provides reliable, ordered, and error-checked delivery of a stream of bytes.",
    "DNS translates human-friendly domain names to IP addresses for routing."
]


def upsert_samples():
    """Compute embeddings and upsert them into the Endee vector DB.

    Each vector is given a random UUID as its id and the original text is
    stored under `metadata.text` so it can be returned during searches.
    """
    for text in SENTENCES:
        emb = get_embedding(text)
        payload = {
            "vectors": [
                {
                    "id": str(uuid.uuid4()),
                    "values": emb,
                    "metadata": {"text": text}
                }
            ]
        }
        try:
            resp = requests.post(ENDEE_UPSERT, json=payload, timeout=10)
            print(f"Upserted: {text[:60]}... status={resp.status_code}")
            print("Response:", resp.text)
        except Exception as e:
            print("Error upserting:", e)


if __name__ == "__main__":
    upsert_samples()
