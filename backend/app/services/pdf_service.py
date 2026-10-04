import pymupdf
from pathlib import Path

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF page by page.

    Returns:
        A list of dictionaries containing page text and metadata.
    """

    document = pymupdf.open(file_path)
    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        if text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    document.close()

    return pages