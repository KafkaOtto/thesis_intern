from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from config import HF_MODEL_NAME
from base import EmbeddingRequest, EmbeddingResponse, EmbeddingMetadata

class EmbeddingService:
    """ Handles embedding generation using a Hugging Face transformer model. """

    def __init__(self):
        print(f"Loading model: {HF_MODEL_NAME} ...")
        self.model = SentenceTransformer(HF_MODEL_NAME)

    def generate_embeddings(self, request: EmbeddingRequest) -> EmbeddingResponse:
        embeddings = self.model.encode(request.inputs, convert_to_numpy=True).tolist()

        if request.options.normalize:
            embeddings = self._normalize_embeddings(embeddings)

        metadata = EmbeddingMetadata(
            model=HF_MODEL_NAME,
            usage={"input_texts": len(request.inputs)}
        )

        return EmbeddingResponse(embeddings=embeddings, metadata=metadata)

    def _normalize_embeddings(self, embeddings: List[List[float]]) -> List[List[float]]:
        """ Normalizes the embeddings to unit length. """
        return [list(np.array(vec) / (np.linalg.norm(vec) + 1e-10)) for vec in embeddings]

embedding_service = EmbeddingService()
