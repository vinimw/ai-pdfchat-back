
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from app.db.database import Base
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
    pages: int
    characters: int
    created_at: datetime

    class Config:
        from_attributes = True


# class DocumentModel(Base):
#     __tablename__ = "documents"

#     document_id = Column(String, primary_key=True, index=True)
#     collection_name = Column(String, nullable=False, unique=True)
#     filename = Column(String, nullable=False)
#     pages = Column(Integer, nullable=False)
#     characters = Column(Integer, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)