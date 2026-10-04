from backend.app.services.embedding_service import generate_embedding
from backend.app.services.vector_service import collection

MAX_DISTANCE = 1.50
def retrieve_relevant_chunks(query: str, top_k: int = 5,) -> list[dict]:
    """
    Retrieve the most relevant chunks from ChromaDB.
    """

    query_embedding = generate_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_chunks = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(documents,metadatas,distances,):
        if distance > MAX_DISTANCE:
            continue
        retrieved_chunks.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks