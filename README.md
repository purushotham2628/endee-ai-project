# Endee Semantic Search System

## Project Overview

This project implements a **Semantic Search System** using the **Endee Vector Database**.  
The system retrieves text based on **meaning**, not just keyword matches, by using vector embeddings and similarity search.

It demonstrates how vector databases can power intelligent search applications without relying on external LLM services.

---

## Problem Statement

Traditional keyword-based search fails when users use different words with the same meaning.  
For example, searching:

> “What does DNS do?”

may not match text like:

> “DNS translates domain names to IP addresses”

because exact keywords differ.

This project solves that problem using **semantic similarity**:
- Text is converted into numerical embeddings
- Similar meanings produce similar vectors
- The vector database retrieves the most semantically relevant results

---

## System Design / Technical Approach

The system consists of four main components:

### 1. Embedding Generation
Text data is converted into **384-dimensional embeddings** using the `sentence-transformers` model (`all-MiniLM-L6-v2`).  
These embeddings represent the semantic meaning of the text.

### 2. Vector Storage (Endee)
The embeddings are stored inside **Endee**, a high-performance vector database.  
Each vector is assigned an ID, and the original text is mapped using a local metadata file.

### 3. Semantic Search
When a user enters a query:
1. The query is converted into an embedding  
2. The embedding is sent to Endee  
3. Endee returns the most similar stored vectors using cosine similarity  

### 4. Result Retrieval
The system maps returned vector IDs back to the original text using `vector_metadata.json` and displays the most relevant results.

---

## How Endee is Used

Endee serves as the **core vector database** in this project.

- Endee is run locally using Docker
- A vector index is created with dimension 384
- Text embeddings are inserted into the Endee index
- Search queries are executed via Endee’s REST API
- Endee performs fast similarity search and returns the closest vectors

This demonstrates real-world usage of Endee for semantic search applications.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Docker installed and running
- Endee server running locally at `http://localhost:8080`

### Step 1 — Start Endee Database

```bash
docker run -p 8080:8080 -v endee-data:/data --name endee-server endeeio/endee-server:latest
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Create Vector Index

```bash
python create_index.py
```

### Step 4 — Store Text Embeddings

```bash
python store_vectors.py
```

### Step 5 — Run Semantic Search

```bash
python search.py
```

Or use the interactive version:

```bash
python rag_chat.py
```

Enter any question, and the system will return the most semantically similar stored text.

---

## Summary

This project demonstrates how **semantic search** can be built using:

- Sentence embeddings  
- A vector database (Endee)  
- Similarity-based retrieval  

It highlights a practical AI/ML use case where vector search is the core component.