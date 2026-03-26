from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentListItemResponse

router = APIRouter(tags=["documents"])


@router.get("/documents", response_model=list[DocumentListItemResponse])
async def list_documents(db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    return repository.list_all()


@router.get("/documents/{document_id}", response_model=DocumentListItemResponse)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    document = repository.get_by_id(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document