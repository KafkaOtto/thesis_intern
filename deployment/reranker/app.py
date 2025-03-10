from fastapi import FastAPI
from base import RerankRequest, RerankResponse
from service import reranker_service

app = FastAPI(title="Hugging Face Embedding API", version="1.0")

@app.post("/rerank", response_model=RerankResponse)
async def generate_embeddings(request: RerankRequest):
    return reranker_service.reranking(request)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Embedding Service (Hugging Face)!"}
