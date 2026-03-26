from datetime import datetime
from pydantic import BaseModel
from app.schemas.chunk import DocumentChunk

class DocumentExtractResponse(BaseModel):
    document_id: str
    collection_name: str
    filename: str
    pages: int
    characters: int
    text: str
    chunks: list[DocumentChunk]


class DocumentListItemResponse(BaseModel):
    document_id: str
    collection_name: str
    filename: str
    stored_filename: str
    file_path: str
    pages: int
    characters: int
    created_at: datetime

    class Config:
        from_attributes = True