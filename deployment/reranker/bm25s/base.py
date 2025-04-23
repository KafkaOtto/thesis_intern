from typing import List, Dict, Any
from pydantic import BaseModel

class RerankRequest(BaseModel):
    query: str
    documents: List[str]
    topN: int = 5
    threshold: float = 0.0

class RerankResult(BaseModel):
    index: int
    relevance_score: float

# Response schema
class RerankResponse(BaseModel):
    results: List[RerankResult]

