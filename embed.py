"""embed.py

Provides a simple wrapper around sentence-transformers to produce
embeddings for text. Uses the `all-MiniLM-L6-v2` model which is
small, fast and suitable for local use.

Install dependency: `pip install sentence-transformers`
"""
from sentence_transformers import SentenceTransformer

# Load the model once at import time so repeated calls are fast.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list:
    """Return a dense vector embedding for `text` as a Python list of floats.

    Args:
        text: Input text to embed.

    Returns:
        A list of floats representing the embedding.
    """
    if text is None:
        return []

    # The model returns a numpy array; convert to plain Python list
    vec = _model.encode(text)
    try:
        return vec.tolist()
    except Exception:
        # Fallback: ensure each element is a Python float
        return [float(x) for x in vec]


if __name__ == "__main__":
    # Quick local demo
    sample = "What is a subnet and why is it useful?"
    emb = get_embedding(sample)
    print(f"Embedding length: {len(emb)}")
