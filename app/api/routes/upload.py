from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(tags=["upload"])


@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    return {
        "filename": file.filename,
        "message": "Upload received successfully"
    }