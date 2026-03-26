from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentExtractResponse
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PdfService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService


class DocumentService:
    @staticmethod
    async def extract_document(file: UploadFile, db: Session) -> DocumentExtractResponse:
        file_bytes = await file.read()
        text, pages = PdfService.extract_text_from_bytes(file_bytes)
        chunks = ChunkService.split_text(text)

        document_id = str(uuid4())
        collection_name = f"document_{document_id}"

        vector_store_service = VectorStoreService(collection_name=collection_name)
        retrieval_service = RetrievalService(
            vector_store_service=vector_store_service
        )
        retrieval_service.index_document(document_id=document_id, chunks=chunks)

        repository = DocumentRepository(db)
        repository.create(
            document_id=document_id,
            collection_name=collection_name,
            filename=file.filename or "unknown.pdf",
            pages=pages,
            characters=len(text),
        )

        return DocumentExtractResponse(
            document_id=document_id,
            collection_name=collection_name,
            filename=file.filename or "unknown.pdf",
            pages=pages,
            characters=len(text),
            text=text,
            chunks=chunks,
        )