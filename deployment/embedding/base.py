from typing import List, Dict, Any
from pydantic import BaseModel

class EmbeddingOptions(BaseModel):
    """ Options for generating embeddings. """
    model: str = "sentence-transformers/all-MiniLM-L6-v2"
    normalize: bool = False

class EmbeddingRequest(BaseModel):
    """ Represents an embedding request with inputs and options. """
    inputs: List[str]
    options: EmbeddingOptions = EmbeddingOptions()

class EmbeddingMetadata(BaseModel):
    """ Metadata related to the embedding response. """
    model: str
    usage: Dict[str, Any]

class EmbeddingResponse(BaseModel):
    """ Stores the embedding response including metadata. """
    embeddings: List[List[float]]
    metadata: EmbeddingMetadata
