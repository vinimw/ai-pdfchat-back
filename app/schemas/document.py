from pydantic import BaseModel

from app.schemas.chunk import DocumentChunk

class DocumentExtractResponse(BaseModel):
    document_id: str
    filename: str
    pages: int
    characters: int
    text: str
    chunks: list[DocumentChunk]