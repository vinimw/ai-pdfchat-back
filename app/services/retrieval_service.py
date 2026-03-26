from app.schemas.chunk import DocumentChunk
from app.schemas.retrieval import RetrievedChunk
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

class RetrievalService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store_service: VectorStoreService | None = None,
    ) -> None:
        self.embedding_service = embedding_service or EmbeddingService()
        self.vector_store_service = vector_store_service or VectorStoreService()

    def index_document(self, document_id: str, chunks: list[DocumentChunk]) -> None:
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = self.embedding_service.embed_texts(chunk_texts)
        self.vector_store_service.index_chunks(document_id, chunks, embeddings)

    def retrieve(
        self,
        document_id: str,
        question: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        query_embedding = self.embedding_service.embed_query(question)
        return self.vector_store_service.search(
            query_embedding=query_embedding,
            document_id=document_id,
            top_k=top_k,
        )