from uuid import uuid4

from fastapi import UploadFile

from app.schemas.document import DocumentExtractResponse
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PdfService
from app.services.retrieval_service import RetrievalService

class DocumentService:
    @staticmethod
    async def extract_document(file: UploadFile) -> DocumentExtractResponse:
        file_bytes = await file.read()
        text, pages = PdfService.extract_text_from_bytes(file_bytes)
        chunks = ChunkService.split_text(text)

        document_id = str(uuid4())
        retrieval_service = RetrievalService()
        retrieval_service.index_document(document_id=document_id, chunks=chunks)

        return DocumentExtractResponse(
            filename=file.filename or "unknown.pdf",
            pages=pages,
            characters=len(text),
            text=text,
            chunks=chunks,
            document_id=document_id,
        )