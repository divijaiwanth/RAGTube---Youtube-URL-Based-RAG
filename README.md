# RAGTube

RAGTube is a Retrieval-Augmented Generation (RAG) system that enables users to ask natural language questions about YouTube videos using their transcripts. The system combines semantic retrieval with a local language model to generate context-aware answers without relying on external paid APIs.

---

## Overview

RAGTube implements an end-to-end RAG pipeline that ingests YouTube transcripts, transforms them into vector embeddings, retrieves relevant context based on user queries, and generates answers using a local LLM.

This project demonstrates practical understanding of modern AI system design, including retrieval pipelines, vector databases, and LLM orchestration.

---

## Architecture


YouTube Video → Transcript → Chunking → Embeddings → FAISS
→ Retrieval → Prompt Augmentation → LLM → Answer


---

## Key Features

- Retrieval-Augmented Generation (RAG) pipeline  
- Semantic search using vector embeddings  
- Context-aware question answering  
- Fully local inference using Ollama (no external APIs)  
- Interactive web interface using Streamlit  

---

## Tech Stack

- **Frontend:** Streamlit  
- **LLM Orchestration:** LangChain  
- **Vector Database:** FAISS  
- **Embeddings:** HuggingFace (sentence-transformers)  
- **LLM Runtime:** Ollama (Mistral)  
- **Data Source:** youtube-transcript-api  

---

## Setup

```bash
git clone https://github.com/divijaiwanth/RAGTube-Youtube-URL-Based-RAG.git
cd RAGTube-Youtube-URL-Based-RAG
```
```bash
python -m venv venv
venv\Scripts\activate
```
```bash
pip install -r requirement.txt
```

Run Local Model
```bash
ollama pull mistral
ollama serve
```

Run Application
```bash
streamlit run main.py
```

Usage
```bash
Enter a YouTube video URL
Input a question related to the video
Submit the query
Receive an answer generated from the transcript context
```

# Design Highlights
Implements a modular RAG pipeline 
(ingestion → retrieval → generation)
Uses chunking with overlap to preserve context during retrieval
Optimized for local execution with no dependency on external APIs

Demonstrates integration of vector search with LLM-based reasoning
Limitations

Works only for videos with available transcripts
Vector database is currently in-memory (not persisted)

Performance depends on transcript quality and chunking strategy
Future Improvements

Persistent vector storage (FAISS save/load)
Multi-video knowledge base

Conversational memory (multi-turn queries)
Hybrid search (keyword + vector)

Reranking for improved retrieval accuracy

License
```bash
This project is intended for educational and experimental purposes.
```