from fastapi import FastAPI
from base import EmbeddingRequest, EmbeddingResponse
from service import embedding_service

app = FastAPI(title="Hugging Face Embedding API", version="1.0")

@app.post("/generate-embeddings", response_model=EmbeddingResponse)
async def generate_embeddings(request: EmbeddingRequest):
    """ Endpoint to generate text embeddings. """
    return embedding_service.generate_embeddings(request)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Embedding Service (Hugging Face)!"}
