from fastapi import UploadFile

from app.schemas.document import DocumentExtractResponse
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PdfService


class DocumentService:
    @staticmethod
    async def extract_document(file: UploadFile) -> DocumentExtractResponse:
        file_bytes = await file.read()
        text, pages = PdfService.extract_text_from_bytes(file_bytes)
        chunks = ChunkService.split_text(text)

        return DocumentExtractResponse(
            filename=file.filename or "unknown.pdf",
            pages=pages,
            characters=len(text),
            text=text,
            chunks=chunks,
        )