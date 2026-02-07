# Endee RAG Project

A simple Python Retrieval-Augmented Generation (RAG) system using a local Endee vector database and OpenAI's GPT API.

## Architecture

1. **Embedding Layer** (`embed.py`) - Converts text to 384-dimensional vectors using `sentence-transformers` all-MiniLM-L6-v2 model
2. **Storage Layer** (`store_vectors.py`) - Inserts embeddings into Endee index and stores metadata locally in `vector_metadata.json`
3. **Retrieval Layer** (`search.py`) - Searches Endee for similar vectors and retrieves metadata from local file
4. **Generation Layer** (`rag_chat.py`) - Uses OpenAI to answer questions based ONLY on retrieved context

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
- OpenAI API key (for RAG chat feature)

### Installation

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...  # Set your OpenAI key
```

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

### 4. RAG Chat (Requires OpenAI API Key)

```bash
python rag_chat.py
```

Complete RAG pipeline:
1. **Search Phase** - Finds relevant vectors for query
2. **Context Extraction** - Loads text from `vector_metadata.json`
3. **Generation** - Calls OpenAI with system prompt ensuring answer uses ONLY provided context
4. **Output** - Returns answer with source attribution

**Example:**
```
Question: What is the purpose of DNS?

[1] Searching for relevant context...
[2] Found 2 matching vectors
[3] Calling OpenAI gpt-3.5-turbo...

[Answer]
DNS translates human-friendly domain names to IP addresses for routing.
```

## Files

| File | Purpose |
|------|---------|
| `embed.py` | Text embedding using sentence-transformers |
| `create_index.py` | Initialize Endee vector index |
| `store_vectors.py` | Insert vectors and save metadata |
| `search.py` | Search and retrieve similar vectors |
| `rag_chat.py` | Complete RAG with OpenAI integration |
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
- `sentence-transformers` - Text embeddings
- `requests` - HTTP client
- `msgpack` - Binary protocol support
- `openai` - OpenAI API client

## Example Workflow

```bash
# 1. Create index (one-time)
python create_index.py

# 2. Store vectors and metadata
python store_vectors.py

# 3. Test search
python search.py

# 4. Run full RAG (requires OpenAI API key)
python rag_chat.py
```

## Notes

- Vectors are stored permanently in Endee (survives restarts)
- Metadata file is regenerated each time `store_vectors.py` runs
- OpenAI calls incur API costs
- Set `temperature=0.0` in `rag_chat.py` for consistent answers
```

### 4. RAG Chat

```bash
export OPENAI_API_KEY=sk-... 
python rag_chat.py
```

Retrieves context and answers using OpenAI based only on that context.

## API Details

### Endee Endpoints Used

**Create Index**
- POST `/api/v1/index/create`
- Payload: `{"index_name": "...", "dim": 384, "space_type": "cosine"}`

**Insert Vectors**
- POST `/api/v1/index/{index_name}/vector/insert`
- Payload: JSON array of `{"id": "...", "vector": [...], "meta": {...}}`

**Search**
- POST `/api/v1/index/{index_name}/search`
- Payload: `{"vector": [...], "k": 2, "include_vectors": true}`
- Response: msgpack-encoded binary data

## File Structure

```
.
├── embed.py              # Text -> Vector (384-dim)
├── create_index.py       # Create Endee index
├── store_vectors.py      # Insert vectors into index
├── search.py             # Search index for similar vectors
├── rag_chat.py           # RAG pipeline: search + OpenAI
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Dependencies

- **sentence-transformers>=2.2.2** - Embedding model
- **requests>=2.28.0** - HTTP client
- **openai>=1.0.0** - OpenAI API client
- **msgpack>=1.0.0** - Binary encoding for responses

## Key Implementation Details

1. **Vector Dimension**: All embeddings are 384-dimensional (all-MiniLM-L6-v2 output)
2. **Similarity Metric**: Cosine similarity for semantic search
3. **Response Format**: Search responses are msgpack-encoded (not JSON)
4. **Context-Only**: RAG system instructs OpenAI to answer only from retrieved context
5. **Temperature**: Set to 0.0 for deterministic responses

## Troubleshooting

**Search returns N/A for text**
- Metadata may not be properly serialized; try re-running `store_vectors.py`

**HTTP 405 errors**
- Verify you're using the correct endpoint path (includes index name)
- Example: `/api/v1/index/notes_index/vector/insert`

**msgpack decode errors**
- Ensure msgpack library is installed: `pip install msgpack`
- Use `msgpack.unpackb(data, raw=False)` for proper string decoding

**OpenAI connection issues**
- Set `OPENAI_API_KEY` environment variable
- Verify API key has access to gpt-3.5-turbo model

## References

- [Endee Vector Database Docs](https://docs.endee.dev/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
