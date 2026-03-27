from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentListItemResponse
from app.services.document_service import DocumentService

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


@router.get("/documents/{document_id}/file")
async def download_document_file(document_id: str, db: Session = Depends(get_db)):
    repository = DocumentRepository(db)
    document = repository.get_by_id(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Stored file not found")

    return FileResponse(
        path=file_path,
        filename=document.filename,
        media_type="application/pdf",
    )


@router.delete("/documents/{document_id}")
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    deleted = DocumentService.delete_document(document_id=document_id, db=db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"message": "Document deleted successfully"}