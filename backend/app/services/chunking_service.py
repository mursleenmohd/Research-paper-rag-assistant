import re

def _word_count(text: str) -> int:
    return len(text.split())

def _split_long_sentence(sentence: str, max_words: int,) -> list[str]:
    """
    Split an unusually long sentence by words.
    """
    words = sentence.split()
    chunks = []
    for start in range(0, len(words),max_words,):
        chunk = " ".join(words[start:start + max_words]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks

def _split_into_sentences(text: str) -> list[str]:
    """
    Basic sentence-aware splitting.
    """
    text = re.sub(r"\s+"," ",text,).strip()
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+",text,)
    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

def split_text(text: str, chunk_size: int = 120, chunk_overlap: int = 20,) -> list[str]:
    """
    Sentence-aware chunking with word-level fallback.
    chunk_size and chunk_overlap are measured in words.
    """

    if not text:
        return []
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    sentences = _split_into_sentences(text)
    units = []

    for sentence in sentences:
        if _word_count(sentence) <= chunk_size:
            units.append(sentence)
        else:
            units.extend(_split_long_sentence(sentence, chunk_size,))

    chunks = []
    current_units = []
    current_words = 0

    for unit in units:
        unit_words = _word_count(unit)
        if (current_units and current_words + unit_words > chunk_size):
            chunks.append(" ".join(current_units).strip())
            overlap_units = []
            overlap_words = 0

            for previous in reversed(current_units):
                previous_words = _word_count(previous)
                if (overlap_words + previous_words > chunk_overlap):
                    break
                overlap_units.insert(0, previous,)
                overlap_words += previous_words
            current_units = overlap_units
            current_words = overlap_words
        current_units.append(unit)
        current_words += unit_words
    if current_units:
        chunks.append(" ".join(current_units).strip())
    return chunks

def create_chunks(pages: list[dict], document_name: str, document_id: str, chunk_size: int = 1000, chunk_overlap: int = 200,) -> list[dict]:
    """
    Create sentence-aware chunks while preserving metadata.
    """
    all_chunks = []
    chunk_index = 0
    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]
        page_chunks = split_text(text=page_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap,)

        for chunk in page_chunks:
            all_chunks.append(
                {
                    "text": chunk,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "document_name": document_name,
                    "document_id": document_id,
                }
            )
            chunk_index += 1
    return all_chunks