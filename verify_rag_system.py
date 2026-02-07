#!/usr/bin/env python
"""
verify_rag_system.py

Verification script to test all components of the RAG system.
Runs independently without OpenAI to verify core functionality.
"""

import json
import os
from pathlib import Path

def verify_files():
    """Check that all required files exist."""
    print("=" * 60)
    print("VERIFYING RAG SYSTEM")
    print("=" * 60)
    print()
    
    required_files = [
        'embed.py',
        'create_index.py',
        'store_vectors.py',
        'search.py',
        'rag_chat.py',
        'vector_metadata.json',
        'requirements.txt'
    ]
    
    print("[1] Checking files...")
    all_exist = True
    for fname in required_files:
        exists = Path(fname).exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {fname}")
        all_exist = all_exist and exists
    
    if not all_exist:
        print("\n  Missing files! Run store_vectors.py first.")
        return False
    
    print()
    return True


def verify_metadata():
    """Check vector metadata file."""
    print("[2] Checking vector metadata...")
    
    try:
        with open('vector_metadata.json', 'r') as f:
            metadata = json.load(f)
        
        print(f"  Found {len(metadata)} vectors:")
        for vec_id, data in metadata.items():
            text = data.get('text', 'N/A')[:50]
            print(f"    - {vec_id}: {text}...")
        
        # Verify expected vectors
        expected = ['vec_001', 'vec_002', 'vec_003']
        all_present = all(v in metadata for v in expected)
        
        if all_present:
            print("  All 3 sample vectors found!")
            print()
            return True
        else:
            print("  Missing expected vectors!")
            return False
    
    except FileNotFoundError:
        print("  vector_metadata.json not found!")
        print("  Run: python store_vectors.py")
        return False
    except json.JSONDecodeError:
        print("  vector_metadata.json is invalid JSON!")
        return False


def verify_imports():
    """Check that required libraries can be imported."""
    print("[3] Checking Python dependencies...")
    
    required_modules = {
        'sentence_transformers': 'sentence-transformers',
        'requests': 'requests',
        'msgpack': 'msgpack',
        'openai': 'openai'
    }
    
    all_installed = True
    for module, package in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - Install with: pip install {package}")
            all_installed = False
    
    print()
    return all_installed


def verify_env():
    """Check environment variables."""
    print("[4] Checking environment...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        masked = api_key[:10] + '...' if len(api_key) > 10 else '...'
        print(f"  ✓ OPENAI_API_KEY is set ({masked})")
    else:
        print("  Note: OPENAI_API_KEY not set")
        print("       RAG chat features will not work")
        print("       Set with: export OPENAI_API_KEY=sk-...")
    
    print()
    return True


def main():
    """Run all verification checks."""
    checks = [
        verify_files(),
        verify_metadata(),
        verify_imports(),
        verify_env()
    ]
    
    print("=" * 60)
    if all(checks):
        print("SUCCESS: RAG system is ready!")
        print()
        print("Next steps:")
        print("  1. Test search:    python search.py")
        print("  2. Test RAG chat:  python rag_chat.py  (needs OpenAI key)")
    else:
        print("ISSUES DETECTED: Please fix errors above")
        print()
        print("Common solutions:")
        print("  - Run: pip install -r requirements.txt")
        print("  - Run: python store_vectors.py")
        print("  - Set: export OPENAI_API_KEY=sk-...")
    print("=" * 60)


if __name__ == "__main__":
    main()
