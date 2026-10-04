from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question to ask about the research documents",)
    top_k: int = Field(default=5, ge=1, le=10, description="Number of relevant chunks to retrieve",)


class Source(BaseModel):
    document_id: str
    document_name: str
    page_number: int
    chunk_index: int
    distance: float


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[Source]