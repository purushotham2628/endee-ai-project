"""create_index.py

Create a vector index in local Endee DB using the correct API.

API endpoint: POST /api/v1/index/create
Payload: {"index_name": "...", "dim": int, "space_type": "cosine", ...}
"""
import requests
import json

ENDEE_URL = "http://localhost:8080"
CREATE_INDEX_URL = f"{ENDEE_URL}/api/v1/index/create"


def create_index(index_name: str = "notes_index", dim: int = 384, space_type: str = "cosine"):
    """
    Create a vector index in Endee.
    
    Args:
        index_name: Name of the index (alphanumeric + underscores, max 48 chars)
        dim: Vector dimension (must match embeddings dimension)
        space_type: Metric type - 'cosine', 'l2', 'inner_product'
    """
    payload = {
        "index_name": index_name,
        "dim": dim,
        "space_type": space_type
    }
    
    print(f"Creating index at: {CREATE_INDEX_URL}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        resp = requests.post(CREATE_INDEX_URL, json=payload, timeout=10)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:500]}")
        
        if resp.status_code in (200, 201):
            print(f"✓ Index '{index_name}' created successfully!")
            return True
        else:
            print(f"✗ Failed to create index. Status {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    create_index()
