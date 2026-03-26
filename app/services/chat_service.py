from typing import Optional

from app.schemas.chat import ChatAskResponse
from app.schemas.retrieval import RetrievedChunk
from app.services.llm_service import LlmService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService


class ChatService:
    def __init__(
        self,
        llm_service: Optional[LlmService] = None,
        retrieval_service: Optional[RetrievalService] = None,
    ) -> None:
        self.llm_service = llm_service or LlmService()
        self.retrieval_service = retrieval_service

    @staticmethod
    def build_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
        context_blocks = []

        for chunk in chunks:
            context_blocks.append(f"[Chunk {chunk.chunk_index}]\n{chunk.text}")

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
        collection_name: str,
        question: str,
        top_k: int = 3,
    ) -> ChatAskResponse:
        retrieval_service = self.retrieval_service or RetrievalService(
            vector_store_service=VectorStoreService(collection_name=collection_name)
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