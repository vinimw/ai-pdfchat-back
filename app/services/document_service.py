from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from app.models.document import DocumentModel
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentExtractResponse
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PdfService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService


class DocumentService:
    STORAGE_DIR = Path("storage/documents")

    @classmethod
    def ensure_storage_dir(cls) -> None:
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    async def extract_document(cls, file: UploadFile, db: Session) -> DocumentExtractResponse:
        cls.ensure_storage_dir()

        original_filename = file.filename or "unknown.pdf"
        file_bytes = await file.read()

        document_id = str(uuid4())
        collection_name = f"document_{document_id}"

        stored_filename = f"{document_id}.pdf"
        stored_path = cls.STORAGE_DIR / stored_filename
        stored_path.write_bytes(file_bytes)

        text, pages = PdfService.extract_text_from_bytes(file_bytes)
        chunks = ChunkService.split_text(text)

        vector_store_service = VectorStoreService(collection_name=collection_name)
        retrieval_service = RetrievalService(vector_store_service=vector_store_service)
        retrieval_service.index_document(document_id=document_id, chunks=chunks)

        repository = DocumentRepository(db)
        repository.create(
            document_id=document_id,
            collection_name=collection_name,
            filename=original_filename,
            stored_filename=stored_filename,
            file_path=str(stored_path),
            pages=pages,
            characters=len(text),
        )

        return DocumentExtractResponse(
            document_id=document_id,
            collection_name=collection_name,
            filename=original_filename,
            pages=pages,
            characters=len(text),
            text=text,
            chunks=chunks,
        )

    @staticmethod
    def get_document_or_raise(document_id: str, db: Session) -> Optional[DocumentModel]:
        repository = DocumentRepository(db)
        return repository.get_by_id(document_id)

    @staticmethod
    def delete_document(document_id: str, db: Session) -> bool:
        repository = DocumentRepository(db)
        document = repository.get_by_id(document_id)

        if not document:
            return False

        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()

        vector_store_service = VectorStoreService(collection_name=document.collection_name)
        try:
            vector_store_service = VectorStoreService(collection_name=document.collection_name)
            vector_store_service.delete_collection()
        except Exception:
            pass

        repository.delete(document)
        return True