# Endee Semantic Search Project

A beginner-friendly Python semantic search system using a local Endee vector database. Embed, store, and search text documents by semantic similarity with zero external LLM dependencies.

## Architecture

1. **Embedding Layer** (`embed.py`) — Converts text to 384-dimensional vectors using `sentence-transformers` all-MiniLM-L6-v2 model
2. **Storage Layer** (`store_vectors.py`) — Inserts embeddings into Endee index and stores metadata locally in `vector_metadata.json`
3. **Retrieval Layer** (`search.py`) — Searches Endee for similar vectors and retrieves metadata from local file
4. **Search CLI** (`rag_chat.py`) — Interactive command-line tool to query and display search results

## Key Design Decisions

### Metadata Storage
Endee's HTTP API does not persist custom metadata fields. Instead, metadata is stored in a local JSON file (`vector_metadata.json`):
- Maps vector IDs to their original text and metadata
- Loaded during search to augment results with context
- Simple and portable solution for small projects

### Response Format
Endee search responses use **msgpack** binary encoding (not JSON):
```python
[similarity_score, vector_id, vector_bytes, metadata_field, norm, spare_indices]
```

## Setup

### Prerequisites
- Python 3.8+
- Endee vector database running at `http://localhost:8080`

### Installation

```bash
pip install -r requirements.txt
```

That's it! No API keys or external service dependencies needed.

## Usage

### 1. Create Vector Index

```bash
python create_index.py
```

Creates `notes_index` with:
- Dimension: 384 (from sentence-transformers model)
- Similarity metric: cosine

### 2. Store Vectors

```bash
python store_vectors.py
```

Processes 3 sample networking sentences:
1. Subnets
2. TCP/IP
3. DNS

Creates:
- Vectors in Endee index (HTTP 200)
- `vector_metadata.json` with text mappings

### 3. Search Vectors

```bash
python search.py
```

Demonstrates search functionality:
- Query: "What does DNS do?"
- Returns: Top 2 similar vectors with cosine scores
- Metadata automatically loaded and displayed

**Output:**
```
Found 2 results:
  1. ID: vec_003, Score: 0.6672
     Text: DNS translates human-friendly domain names to IP addresses...
  2. ID: vec_002, Score: 0.1754
     Text: TCP provides reliable, ordered, and error-checked delivery...
```

### 4. Search Interactively

```bash
python rag_chat.py
```

Interactive CLI that prompts for queries and displays results:
- Converts your question to an embedding
- Searches Endee for semantic matches
- Displays results with similarity scores and original text

**Example:**
```
SEMANTIC SEARCH DEMO
This demo asks for a user question, searches the Endee index, and prints top matches.

Enter your question: What is DNS?

Top 2 matches:
  1. ID: vec_003, Score: 0.6672
     Text: DNS translates human-friendly domain names to IP addresses...

  2. ID: vec_002, Score: 0.1754
     Text: TCP provides reliable, ordered, and error-checked delivery...
```

## Files

| File | Purpose |
|------|---------|
| `embed.py` | Text embedding using sentence-transformers |
| `create_index.py` | Initialize Endee vector index |
| `store_vectors.py` | Insert vectors and save metadata |
| `search.py` | Search and retrieve similar vectors |
| `rag_chat.py` | Interactive semantic search CLI |
| `vector_metadata.json` | Local metadata store (auto-generated) |
| `requirements.txt` | Python dependencies |

## API Endpoints Used

- **Create Index**: `POST /api/v1/index/create`
- **Insert Vectors**: `POST /api/v1/index/{indexName}/vector/insert`
- **Search**: `POST /api/v1/index/{indexName}/search` (returns msgpack)

## Troubleshooting

### Search returns "Text: N/A"
- Ensure `vector_metadata.json` exists
- Run `store_vectors.py` to regenerate it
- Check vector IDs match between Endee and metadata file

### OpenAI API Error
- Verify `OPENAI_API_KEY` environment variable is set
- Check API key is valid at https://platform.openai.com/account/api-keys
- Ensure you have API credits available

### Connection refused (Endee)
- Verify Endee is running at `http://localhost:8080`
- Check Endee logs for errors
- Try manually accessing: `curl http://localhost:8080/`

## Requirements

See `requirements.txt`:
- `sentence-transformers` — Text embedding model (384-dim vectors)
- `requests` — HTTP client for Endee API calls
- `msgpack` — Binary protocol support for Endee responses

## Example Workflow

```bash
# 1. Create index (one-time setup)
python create_index.py

# 2. Store vectors and metadata
python store_vectors.py

# 3. Test search
python search.py

# 4. Interactive search CLI
python rag_chat.py
```

## Key Features

- **Local-first** — No external API dependencies; everything runs on your machine
- **Fast semantic search** — Find similar documents by meaning, not just keywords
- **Lightweight** — Small footprint with only 3 core Python dependencies
- **Educational** — Clean, readable code perfect for learning vector databases and embeddings
- **Extensible** — Easy to add your own documents and index custom data
```

## Key Implementation Details

1. **Vector Dimension**: All embeddings are 384-dimensional (all-MiniLM-L6-v2 model)
2. **Similarity Metric**: Cosine similarity for semantic search
3. **Response Format**: Search responses use msgpack binary encoding
4. **Metadata Storage**: Local JSON file (`vector_metadata.json`) persists document text since Endee doesn't store custom metadata
5. **No External Dependencies**: Uses only requests, sentence-transformers, and msgpack

## Troubleshooting

### Search returns "Text: N/A"
- Ensure `vector_metadata.json` exists (should be auto-generated by `store_vectors.py`)
- Run `python store_vectors.py` again to regenerate metadata
- Check that vector IDs in Endee match those in the metadata file

### Connection refused (Endee)
- Verify Endee is running at `http://localhost:8080`
- Check Endee logs for errors
- Try manually accessing: `curl http://localhost:8080/`

### msgpack decode errors
- Ensure msgpack library is installed: `pip install msgpack`
- Verify Endee responses are in msgpack format (binary, not JSON)
- Try using `msgpack.unpackb(data, raw=False)` for proper string decoding

### Import errors after installation
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.8 or higher: `python --version`

## References

- [Endee Vector Database](https://www.endee.dev/) — Local vector database for semantic search
- [Sentence Transformers](https://www.sbert.net/) — State-of-the-art text embedding models
- [Semantic Search Explained](https://en.wikipedia.org/wiki/Semantic_search) — How semantic search works
- [Vector Embeddings](https://huggingface.co/course/chapter5/1) — Understanding embeddings
