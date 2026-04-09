from typing import Optional

from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.schemas.chat import ChatAskResponse
from app.schemas.retrieval import RetrievedChunk
from app.services.llm_service import LlmService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService


class ChatService:
    def __init__(
        self,
        db: Optional[Session] = None,
        llm_service: Optional[LlmService] = None,
        retrieval_service: Optional[RetrievalService] = None,
    ) -> None:
        self.db = db
        self.llm_service = llm_service or LlmService()
        self.retrieval_service = retrieval_service

    @staticmethod
    def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
        context_blocks = [
            f"[Chunk {chunk.chunk_index}]\n{chunk.text}"
            for chunk in chunks
        ]
        context = "\n\n".join(context_blocks)

        return f"""
You are a document assistant.

Answer the user's question using ONLY the context below.
If the answer is not clearly present in the context, say:
"I could not find enough information in the provided document."

Context:
{context}

Question:
{question}

Answer:
""".strip()

    def ask(
        self,
        document_id: str,
        question: str,
        top_k: int = 3,
        collection_name: Optional[str] = None,
    ) -> ChatAskResponse:
        resolved_collection_name = collection_name

        if self.db is not None:
            repository = DocumentRepository(self.db)
            document = repository.get_by_id(document_id)

            if not document:
                raise ValueError("Document not found")

            resolved_collection_name = document.collection_name

        retrieval_service = self.retrieval_service or RetrievalService(
            vector_store_service=VectorStoreService(
                collection_name=resolved_collection_name or f"document_{document_id}"
            )
        )

        retrieved_chunks = retrieval_service.retrieve(
            document_id=document_id,
            question=question,
            top_k=top_k,
        )

        prompt = self.build_prompt(question, retrieved_chunks)
        answer = self.llm_service.generate(prompt)

        return ChatAskResponse(
            answer=answer,
            sources=retrieved_chunks,
        )
