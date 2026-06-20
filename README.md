# AI Research Assistant (RAG)

A Retrieval-Augmented Generation (RAG) application for querying scientific research papers using local Large Language Models.

## Features

* Download research papers from arXiv
* Extract and clean PDF text
* Sentence-based chunking
* Generate embeddings using Sentence Transformers
* Semantic retrieval using FAISS
* Question answering using Ollama (Llama 3.1)
* Source-aware responses with document citations
* SQLite-based metadata and chunk storage (in progress)

## Tech Stack

* Python
* PyMuPDF
* Sentence Transformers
* FAISS
* Ollama
* Llama 3.1
* SQLite
* SQLAlchemy

## Project Structure

```text
jobs/
ingestion/
indexing/
rag/
storage/
```

## Current Workflow

1. Download research papers from arXiv
2. Store paper metadata
3. Extract and clean text
4. Chunk document content
5. Generate embeddings
6. Store embeddings in FAISS
7. Retrieve relevant chunks
8. Generate answers using Llama 3.1

## Future Improvements

* FastAPI integration
* Streamlit UI
* Automated paper ingestion via RSS feeds
* RAG evaluation framework
* Deployment using Docker
* Migration to a metadata-aware vector database

## Example Query

```text
What are limitations of LLMs in community search problems?
```

## Status

Active personal project under development.
