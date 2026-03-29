from datetime import datetime
from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)

    document_id: str
    collection_name: str
    filename: str
    stored_filename: str
    file_path: str
    pages: int
    characters: int
    created_at: datetime
