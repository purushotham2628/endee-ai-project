"""search.py

Search the Endee index for vectors similar to a query embedding.

API endpoint: POST /api/v1/index/{indexName}/search
Payload: {"vector": [...], "k": int, "include_vectors": bool, ...}
Response: msgpack-encoded list of results

Metadata is loaded from vector_metadata.json (stored locally since Endee API doesn't persist it)
"""
import requests
import json
import msgpack
from embed import get_embedding

ENDEE_URL = "http://localhost:8080"
INDEX_NAME = "notes_index"
SEARCH_URL = f"{ENDEE_URL}/api/v1/index/{INDEX_NAME}/search"
METADATA_FILE = "vector_metadata.json"

# Load metadata from local file
def load_metadata():
    """Load vector metadata from local JSON file."""
    try:
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {METADATA_FILE} not found. Run store_vectors.py first.")
        return {}


def search(query: str, top_k: int = 2) -> dict:
    """
    Search the index for vectors similar to the query.
    
    Args:
        query: Text query to search for
        top_k: Number of top results to return (max 512)
    
    Returns:
        dict with 'success' flag and 'results' list with matches
    """
    # Load metadata from local file
    metadata_map = load_metadata()
    
    # Convert query text to embedding
    query_vec = get_embedding(query)
    print(f"Query: {query}")
    print(f"Query embedding dimension: {len(query_vec)}")
    
    # Prepare search payload
    payload = {
        "vector": query_vec,  # Query embedding (list of floats)
        "k": top_k,  # Number of results
        "include_vectors": True  # Include vectors in response
    }
    
    print(f"\nSearching at: {SEARCH_URL}")
    
    try:
        resp = requests.post(SEARCH_URL, json=payload, timeout=10)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code in (200, 201):
            # Decode msgpack response
            decoded = msgpack.unpackb(resp.content, raw=False)
            print(f"\nFound {len(decoded)} results:")
            
            results = []
            for i, result_list in enumerate(decoded, 1):
                # msgpack response: [score, id, vector_bytes, metadata_string, ...]
                if isinstance(result_list, list) and len(result_list) >= 2:
                    similarity = result_list[0]
                    vec_id = result_list[1]
                    
                    # Get metadata from local file using vector ID
                    meta = metadata_map.get(vec_id, {})
                    text = meta.get("text", "N/A") if isinstance(meta, dict) else "N/A"
                    
                    print(f"  {i}. ID: {vec_id}, Score: {similarity:.4f}")
                    print(f"     Text: {text}")
                    
                    results.append({
                        "id": vec_id,
                        "similarity": similarity,
                        "meta": meta,
                        "text": text
                    })
            
            return {"success": True, "results": results}
        else:
            print(f"Error response: {resp.status_code}")
            return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        print(f"Request failed: {e}")
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("="*60)
    print("SEARCH DEMO")
    print("="*60)
    result = search("What does DNS do?")
    if not result.get("success"):
        print("\nSearch failed. Make sure:")
        print("  1. Index 'notes_index' exists (run create_index.py)")
        print("  2. Vectors are stored (run store_vectors.py)")
        print("  3. vector_metadata.json exists")
    print("SEARCH DEMO")
    print("="*60)
    result = search("What does DNS do?")
    if not result.get("success"):
        print("\n⚠ Search failed. Make sure:")
        print("  1. Index 'notes_index' exists (run create_index.py)")
        print("  2. Vectors have been inserted (run store_vectors.py)")
