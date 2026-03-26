from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.exceptions import EmptyPdfError, InvalidPdfError
from app.services.document_service import DocumentService

router = APIRouter(tags=["upload"])


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        return await DocumentService.extract_document(file)
    except InvalidPdfError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except EmptyPdfError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc