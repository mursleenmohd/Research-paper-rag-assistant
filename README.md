# Research Paper RAG Assistant

A Retrieval-Augmented Generation (RAG) based AI assistant that allows users to upload research papers in PDF format and ask questions about their content.
The system extracts text from research papers, creates meaningful chunks, generates embeddings, stores them in ChromaDB, retrieves relevant context using semantic search, and generates grounded answers using a Groq-powered LLM.

---

## Screenshots

### API Documentation

<img width="1906" height="965" alt="image" src="https://github.com/user-attachments/assets/93cc1d31-9155-40a7-9e21-de1cc3a73414" />

Recommended screenshots:

 <img width="1492" height="942" alt="image" src="https://github.com/user-attachments/assets/c102a2e1-6865-4a04-825b-ca6bf465fda3" />

 <img width="1917" height="972" alt="image" src="https://github.com/user-attachments/assets/3d7fd6c3-c09e-485c-99c3-6b383e8196e6" />

---

## Features

### PDF Processing

- Upload research papers in PDF format
- Extract text from PDF pages using PyMuPDF
- Preserve page-level information
- Handle text-based research papers

### Text Chunking

- Split extracted document text into smaller chunks
- Maintain page information for every chunk
- Support chunk overlap for better retrieval context
- Store chunk-level metadata

### Embeddings

- Generate semantic embeddings using SentenceTransformers
- Convert document chunks and user queries into vector representations
- Enable semantic similarity search

### Vector Database

- Persistent ChromaDB storage
- Store document chunks, embeddings, and metadata
- Semantic similarity retrieval
- Persistent local vector database

### Retrieval

- Retrieve the most relevant chunks for a user query
- Configurable `top_k`
- Retrieval distance threshold
- Filter low-relevance results before sending context to the LLM

### LLM-Powered Answers

- Generate answers using Groq LLMs
- Provide retrieved document context to the model
- Reduce unsupported answers by grounding responses in retrieved content
- Return a fallback message when relevant context cannot be found

### Source Tracking

Each retrieved source contains:

- Document ID
- Document name
- Page number
- Chunk index
- Retrieval distance

This allows users to understand where the answer came from.

### Duplicate Document Detection

Documents are identified using a SHA-256 content hash.

This means the same PDF can be detected even if the filename changes.

For example:
 
## Architecture

```text
┌─────────────────────┐
│        User         │
│  Upload PDF / Query │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Streamlit UI     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     FastAPI API     │
└──────────┬──────────┘
           │
 ┌─────────┴──────────────────────┐
 │                                │
 ▼                                ▼
PDF Ingestion               User Question
 │                                │
 ▼                                ▼
PyMuPDF Extraction          Query Embedding
 │                                │
 ▼                                ▼
Chunking                         ChromaDB
 │                                │
 ▼                                ▼
SentenceTransformers         Semantic Retrieval
 │                                │
 ▼                                ▼
Embeddings                  Relevant Chunks
 │                                │
 ▼                                ▼
ChromaDB                     Context Construction
                                  │
                                  ▼
                               Groq LLM
                                  │
                                  ▼
                            Answer + Sources
```

---

## RAG Pipeline

The project follows a standard Retrieval-Augmented Generation pipeline broken down into two core phases:

### 1. Document Ingestion
```text
PDF Document ➔ Text Extraction (PyMuPDF) ➔ Chunking ➔ Embedding Generation (SentenceTransformers) ➔ ChromaDB Vector Store
```

### 2. Question Answering
```text
User Question ➔ Query Embedding ➔ Semantic Search (ChromaDB) ➔ Relevant Chunks ➔ Distance Filtering ➔ Context Construction ➔ Groq LLM ➔ Final Answer + Sources
```

---

## Project Structure

```text
research-paper-rag-assistant/
│
├── backend/
│   ├── app/ 
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   └── routes.py
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_service.py
│   │   │   ├── retrieval_service.py
│   │   │   ├── llm_service.py
│   │   │   └── document_service.py
│   │   │
│   │   ├── models/
│   │   │   └── schemas.py
│   │   │
│   │   └── core/
│   │       └── config.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └─app.py
│
├── data/
│   ├── uploads/
│   └── chroma/
├
├── .env
├── .gitignore
```

---

## Environment Variables

API credentials and configurations are securely managed using environment variables instead of hardcoding secrets. Create a `.env` file in the root directory based on the configuration below:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# App Configurations
BACKEND_URL=http://localhost:8000
DATABASE_PATH=./data/chroma
UPLOAD_DIR=./data/uploads
```

---

## Getting Started

### Prerequisites
* Python 3.10 or higher
* Groq API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mursleenmohd/Research-paper-rag-assistant.gt
   cd research-paper-rag-assistant
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Open .env and add your GROQ_API_KEY
   ```

3. **Install Backend Dependencies & Run:**
   ```bash
   cd backend
   python -m venv myenv
   myenv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. **Install Frontend Dependencies & Run:**
   Open a new terminal session, navigate to the project directory, and run:
   ```bash
   pip install streamlit requests
   streamlit run frontend/app.py
   ```

---

# Research Paper RAG Assistant

Built as a hands-on project to learn and implement Retrieval-Augmented Generation systems using Python and modern AI tooling.

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **FastAPI** | Backend REST API |
| **Streamlit** | Frontend interface |
| **ChromaDB** | Vector database |
| **SentenceTransformers** | Embeddings |
| **PyMuPDF** | PDF text extraction |
| **Groq** | LLM inference |
| **Pydantic** | Request/response validation |
| **Uvicorn** | ASGI server |
| **python-dotenv** | Environment variable management |

---

## Example Questions

After uploading a research paper, users can ask questions such as:
* What is the main objective of this research paper?
* What methodology or approach does the paper propose?
* What are the main findings of the research?
* What dataset was used in the study?
* What are the limitations mentioned by the authors?

The system retrieves relevant chunks from the paper before generating an answer.

---

### 1. Duplicate Document Detection
The system generates a **SHA-256 hash** from the PDF content to prevent redundant storage. Renaming a file does not create a new document identity because both files produce the same unique `document_id`.

```text
PDF Content ──> SHA-256 ──> Document ID ──> ChromaDB Storage
```
*Example:* `paper.pdf` and `paper-final.pdf` (with identical content) resolve to the exact same `document_id`.

### 2. Retrieval Filtering
The retriever enforces a strict distance threshold to eliminate insufficiently relevant context chunks before passing data to the LLM.
*   **Current Configuration:** `MAX_DISTANCE = 1.50`
*   **Impact:** Reduces the risk of generating answers from unrelated document sections.

### 3. Hallucination Reduction
To maximize accuracy and ensure grounded outputs, the project employs several safety techniques:
*   Retrieval before generation
*   Semantic similarity search & retrieval distance filtering
*   Limited `top_k` context windows
*   Context-based prompt engineering
*   Source metadata mapping
*   Graceful fallback responses when no relevant chunks are retrieved

---

## Project Roadmap

### Version 1 — Research Paper RAG (Current)
```text
PDF ──> Chunking ──> Embeddings ──> ChromaDB ──> Retrieval ──> LLM ──> Answer + Sources
```

### Version 2 — Agentic Research Assistant (Future)
```text
User ──> Research Agent ──> Planning ──> Paper RAG + Web Search + Tools ──> Evidence Verification ──> Synthesis ──> Cited Research Answer
```

---

## Future Improvements

### 1. Advanced Retrieval Techniques
*   **Hybrid Search:** Combine BM25 keyword matching with vector search.
*   **Reranking:** Implement Cross-Encoder reranking models.
*   **Advanced Chunking:** Transition to parent-child retrieval and better semantic chunking strategies.
*   **Query Expansion:** Introduce query rewriting and multi-query retrieval.

### 2. Agentic RAG & Frameworks
*   **LangChain Integration:** Utilize LangChain for LLM abstractions, retriever integrations, tool calling, and prompt management.
*   **LangGraph Workflows:** Build a stateful research workflow loop:
    ```text
    START ──> Understand Query ──> Create Research Plan ──> Retrieve Documents ──> Search Web (If Needed) ──> Evaluate Evidence ──> Synthesize ──> Final Answer
    ```
*   **Tool Choice:** Allow an AI agent to dynamically decide between querying the Paper RAG, performing a Web Search, or running an Evidence Check.

### 3. Advanced Research & Production Features
*   **Research Capabilities:** Multi-document research, cross-paper comparison, citation graph tracking, automatic literature reviews, and figure/table understanding.
*   **Enterprise Infrastructure:** Backend authentication, rate limiting, async processing with background jobs, API versioning, caching, and migrate to a production-grade vector database via Docker.
*   **Observability:** Enhanced logging, token usage tracking, and latency monitoring.

---

## Evaluation Suite
Future iterations will introduce an automated evaluation matrix to measure the following metrics:
*   Retrieval accuracy & context relevance
*   Answer correctness & faithfulness
*   Citation accuracy, latency, and token usage

### Evaluation Dataset Structure:

| Question | Expected Answer | Relevant Page | Retrieved Page | Generated Answer | Correct / Incorrect |
| :--- | :--- | :--- | :--- | :--- | :--- |

---

## Current Limitations
This project is currently designed as a learning and portfolio-focused RAG system. The following limitations are intentionally left for future iterations:
*   Primarily focused on text-based PDFs (no OCR pipeline for scanned documents).
*   Local ChromaDB storage with no active cloud deployment or authentication.
*   No advanced reranking, web research agents, or multi-agent workflows.

---

## Learning Goals
This project was built to master the core fundamentals of modern RAG architecture:
*   Document ingestion, PDF processing, and chunking strategies.
*   Embedding generation and vector database management.
*   Semantic retrieval, distance filtering, and prompt grounding.
*   API deployment with FastAPI, frontend design with Streamlit, and document deduplication.

---

**Author:** Mursleen  
*Built as a portfolio project to explore modern Retrieval-Augmented Generation workflows.*

