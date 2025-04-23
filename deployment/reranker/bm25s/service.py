import bm25s
import Stemmer
from base import RerankRequest, RerankResponse, RerankResult

class RerankerService:
    def __init__(self):
        self.stemmer = Stemmer.Stemmer("english")
        self.retriever = bm25s.BM25()

    def reranking(self, request: RerankRequest) -> RerankResponse:
        print(f"RerankerService.reranking: {request}")
        doc_len = len(request.documents)
        if doc_len == 0:
            return RerankResponse(results=[])
        top_n = min(request.topN, doc_len)
        print(f"RerankerService.reranking doc_len: {doc_len}, top_n: {top_n}")
        corpus_tokens = bm25s.tokenize(request.documents, stopwords="en", stemmer=self.stemmer)
        self.retriever.index(corpus_tokens)
        query_tokens = bm25s.tokenize(request.query, stemmer=self.stemmer)
        results, scores = self.retriever.retrieve(query_tokens, k=top_n)
        print(f"RerankerService.reranking results: {results}")
        print(f"RerankerService.reranking scores: {scores}")
        threshold = request.threshold if request.threshold is not None else 0.0
        filtered_results = []
        for i in range(results.shape[1]):
            doc, score = results[0, i], scores[0, i]
            if score >= threshold:
                filtered_results.append(RerankResult(index=doc, relevance_score=float(score)))

        return RerankResponse(results=filtered_results)

reranker_service = RerankerService()
