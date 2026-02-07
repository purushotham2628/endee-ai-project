# Simple Python RAG with Endee (local) and OpenAI

This small project demonstrates a Retrieval-Augmented Generation (RAG)
workflow using a local Endee vector DB (assumed at `http://localhost:8080`) for
retrieval and OpenAI for generation.

Files
- `embed.py`: Build embeddings with `sentence-transformers`.
- `store_vectors.py`: Upsert three sample networking sentences to Endee.
- `search.py`: Search Endee by converting a query into an embedding.
- `rag_chat.py`: Combine retrieved context and ask OpenAI to answer using only that context.
- `requirements.txt`: Python dependencies.

Prerequisites
- Python 3.8+
- Endee vector DB running at `http://localhost:8080`
- OpenAI API key (for generation)

Install
```bash
pip install -r requirements.txt
```

Populate the vector DB
1. Start your Endee server on `localhost:8080`.
2. Run:

```bash
python store_vectors.py
```

This will compute embeddings for three sample networking sentences and
upsert them into Endee with the original text saved in `metadata.text`.

Run the RAG example
Set your OpenAI API key (PowerShell):

```powershell
$env:OPENAI_API_KEY = "sk-..."
python rag_chat.py
```

Notes
- The code is intentionally simple and beginner-friendly. See inline
  comments for guidance.
- If Endee's API shape differs, you may need to adjust `store_vectors.py`
  or `search.py` to match the exact request/response fields.
