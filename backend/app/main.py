from fastapi import FastAPI
from backend.app.api.routes import router

app = FastAPI(
    title="Research RAG Assistant",
    description="AI assistant for research papers and PDF documents",
    version="0.1.0",
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Research RAG Assistant API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }