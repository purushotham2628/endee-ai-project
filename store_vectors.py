"""store_vectors.py

Upsert sample networking sentences into the Endee index.
Also save metadata locally in a JSON file for retrieval during search.

API endpoint: POST /api/v1/index/{indexName}/vector/insert
Payload: List of vectors with id, vector (array of floats)

Note: Endee doesn't support storing arbitrary metadata through the API,
so we maintain a local metadata file: vector_metadata.json
"""
import requests
import json
from embed import get_embedding

ENDEE_URL = "http://localhost:8080"
INDEX_NAME = "notes_index"
INSERT_URL = f"{ENDEE_URL}/api/v1/index/{INDEX_NAME}/vector/insert"
METADATA_FILE = "vector_metadata.json"

# Sample networking sentences to embed and store
SENTENCES = [
    "A subnet divides a network into smaller, more manageable pieces.",
    "TCP provides reliable, ordered, and error-checked delivery of a stream of bytes.",
    "DNS translates human-friendly domain names to IP addresses for routing."
]


def store_samples():
    """
    Embed and insert sample sentences into the notes_index.
    Store metadata locally in vector_metadata.json since Endee API doesn't support it.
    
    Note: Make sure the index exists first by running create_index.py
    """
    print(f"Inserting {len(SENTENCES)} vectors into '{INDEX_NAME}'...\n")
    
    # Dictionary to store metadata locally
    metadata_map = {}
    
    for i, text in enumerate(SENTENCES, start=1):
        # Get embedding for this text
        vec = get_embedding(text)
        vector_id = f"vec_{i:03d}"
        
        print(f"Vector {i}: {text[:50]}...")
        print(f"  ID: {vector_id}")
        print(f"  Embedding dimension: {len(vec)}")
        print(f"  Text: {text}")
        
        # Store metadata locally (Endee doesn't support metadata via API)
        metadata_map[vector_id] = {
            "text": text,
            "index": i
        }
        
        # Prepare payload: list of vector objects
        # Only include id and vector - Endee API doesn't persist custom metadata
        payload = [
            {
                "id": vector_id,  # Unique vector ID
                "vector": vec,     # The embedding (list of floats)
            }
        ]
        
        print(f"  Sending to: {INSERT_URL}")
        
        try:
            resp = requests.post(INSERT_URL, json=payload, timeout=10)
            print(f"  Status: {resp.status_code}")
            
            if resp.status_code in (200, 201):
                print(f"  ✓ Inserted successfully\n")
            else:
                print(f"  ✗ Failed. Response: {resp.text[:200]}\n")
        except Exception as e:
            print(f"  ✗ Error: {e}\n")
    
    # Save metadata to local file
    print(f"Saving metadata to {METADATA_FILE}...")
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata_map, f, indent=2)
    print(f"✓ Metadata saved!\n")
    
    print("Done!")


if __name__ == "__main__":
    store_samples()


if __name__ == "__main__":
    store_samples()
