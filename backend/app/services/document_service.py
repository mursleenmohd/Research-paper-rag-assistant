from pathlib import Path
import hashlib
from fastapi import HTTPException, UploadFile

UPLOAD_DIR = Path("data/uploads")
MAX_FILE_SIZE = 20 * 1024 * 1024 

def validate_pdf(file: UploadFile) -> None:
    """
    Validate uploaded file.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.",)
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.",)


async def read_pdf_bytes(file: UploadFile) -> bytes:
    """
    Read and validate PDF size.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded PDF is empty.",)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="PDF file is too large. Maximum size is 20 MB.",)
    return content

def generate_document_id(content: bytes) -> str:
    """
    Generate a stable ID from PDF content.
    Same PDF content = same document ID,
    even if the filename changes.
    """
    return hashlib.sha256(content).hexdigest()

def get_storage_path(document_id: str) -> Path:
    """
    Generate a safe server-side PDF path.
    """

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True,)
    return UPLOAD_DIR / f"{document_id}.pdf"

def save_pdf(content: bytes, document_id: str,) -> Path:
    """
    Save PDF using server-generated document ID.
    """

    file_path = get_storage_path(document_id)
    file_path.write_bytes(content)
    return file_path