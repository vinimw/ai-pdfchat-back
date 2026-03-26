from app.schemas.chunk import DocumentChunk
from app.services.retrieval_service import RetrievalService


class FakeEmbeddingService:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[float(i + 1), 0.0, 0.0] for i, _ in enumerate(texts)]

    def embed_query(self, text: str) -> list[float]:
        return [1.0, 0.0, 0.0]


def test_retrieval_service_should_index_and_retrieve() -> None:
    service = RetrievalService(embedding_service=FakeEmbeddingService())

    chunks = [
        DocumentChunk(index=0, text="Python is used for APIs", start_char=0, end_char=24),
        DocumentChunk(index=1, text="FastAPI is a Python framework", start_char=25, end_char=54),
    ]

    service.index_document("doc-test", chunks)
    results = service.retrieve("doc-test", "What is FastAPI?", top_k=2)

    assert len(results) > 0