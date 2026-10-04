import chromadb

CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "research_documents"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def document_already_indexed(document_id: str,) -> bool:
    """
    Check whether this exact PDF has already been indexed.
    """
    result = collection.get(where={"document_id": document_id},limit=1,)
    return bool(result.get("ids"))

def add_chunks(chunks: list[dict], embeddings: list[list[float]],) -> int:
    """
    Store chunks, embeddings and metadata in ChromaDB.
    """

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must be equal."
        )

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        chunk_id = (
            f"{chunk['document_id']}_"
            f"{chunk['chunk_index']}"
        )

        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append(
            {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas,)
    return len(chunks)

def get_collection_count() -> int:
    return collection.count()