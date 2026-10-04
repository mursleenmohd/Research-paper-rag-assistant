from pathlib import Path
import hashlib
from fastapi import APIRouter, File, UploadFile, HTTPException
from backend.app.services.pdf_service import extract_text_from_pdf
from backend.app.services.chunking_service import create_chunks
from backend.app.services.embedding_service import generate_embeddings
from backend.app.services.document_service import (validate_pdf, read_pdf_bytes, generate_document_id, save_pdf,)
from backend.app.services.vector_service import (add_chunks, get_collection_count, document_already_indexed,)
from backend.app.services.retrieval_service import (retrieve_relevant_chunks)
from backend.app.services.llm_service import generate_answer
from backend.app.models.schemas import (AskRequest, AskResponse,)

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def validate_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    validate_pdf(file)

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename,
        "path": str(file_path)
    }

@router.post("/extract-text")
async def extract_pdf_text(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    pages = extract_text_from_pdf(str(file_path))

    return {
        "filename": file.filename,
        "total_pages_with_text": len(pages),
        "pages": pages,
    }

@router.post("/chunk-pdf")
async def chunk_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    pages = extract_text_from_pdf(str(file_path))
    chunks = create_chunks(pages=pages,document_name=file.filename, document_id=document_id,chunk_size=1000,chunk_overlap=200,)
    return {
        "filename": file.filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "chunks": chunks,
    }

@router.post("/ingest-pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    validate_pdf(file)
    content = await read_pdf_bytes(file)
    document_id = hashlib.sha256(content).hexdigest()
    original_filename = file.filename
    if document_already_indexed(document_id):
        return {
            "message": "PDF is already indexed.",
            "filename": original_filename,
            "document_id": document_id,
            "already_indexed": True,
        }
    file_path = save_pdf(content=content, document_id=document_id,)
    pages = extract_text_from_pdf(str(file_path))

    if not pages:
        raise HTTPException(status_code=400, detail="Could not extract text from this PDF.",)

    chunks = create_chunks(pages=pages,document_name=original_filename,document_id=document_id,chunk_size=120,chunk_overlap=20,)
    if not chunks:
        raise HTTPException(status_code=400, detail="No usable text chunks found.",)

    texts = [chunk["text"]
        for chunk in chunks
    ]
    embeddings = generate_embeddings(texts)
    stored_count = add_chunks(chunks=chunks,embeddings=embeddings,)

    return {
        "message": "PDF ingested successfully",
        "filename": original_filename,
        "document_id": document_id,
        "pages": len(pages),
        "chunks": len(chunks),
        "stored_in_chroma": stored_count,
        "already_indexed": False,
    }

@router.get("/retrieve")
def retrieve(query: str, top_k: int = 5,):
    results = retrieve_relevant_chunks(query=query, top_k=top_k,)
    return {
        "query": query,
        "results": results,
    }

@router.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 10.")

    retrieved_chunks = retrieve_relevant_chunks(query=query, top_k=request.top_k,)
    if not retrieved_chunks:
        return {
            "query": query,
            "answer": (
                "I could not find the answer "
                "in the provided documents."
            ),
            "sources": [],
        }
    context_parts = []
    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        context_parts.append(
            f"""
Document: {metadata["document_name"]}
Page: {metadata["page_number"]}

{chunk["text"]}
"""
        )

    context = "\n\n---\n\n".join(context_parts)
    answer = generate_answer(question=query, context=context,)

    return {
        "query": query,
        "answer": answer,
        "sources": [
            {
                "document_id": chunk["metadata"].get("document_id", ""),
                "document_name": chunk["metadata"]["document_name"],
                "page_number": chunk["metadata"]["page_number"],
                "chunk_index": chunk["metadata"]["chunk_index"],
                "distance": chunk["distance"],
            }
            for chunk in retrieved_chunks
        ],
    }