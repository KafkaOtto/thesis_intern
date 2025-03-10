from sentence_transformers import CrossEncoder
from config import HF_MODEL_NAME
from base import RerankRequest, RerankResponse, RerankResult

class RerankerService:
    def __init__(self):
        print(f"Initializing Reranker Service: {HF_MODEL_NAME}")
        self.model = CrossEncoder(HF_MODEL_NAME)

    def reranking(self, request: RerankRequest) -> RerankResponse:
        print(f"threshold: {request.threshold}")
        results = self.model.rank(request.query, request.documents, return_documents=False, top_k=request.topk)

        print(results)
        filtered_results = [
            RerankResult(index=result['corpus_id'], relevance_score=float(result['score']))
            for result in results if float(result['score']) >= request.threshold
        ]

        return RerankResponse(rankings=filtered_results)

reranker_service = RerankerService()
