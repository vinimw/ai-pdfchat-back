from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.query import QueryRequest
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(tags=["query"])


@router.post("/documents/query")
async def query_document(
    payload: QueryRequest,
    db: Session = Depends(get_db),
):
    repository = DocumentRepository(db)
    document = repository.get_by_id(payload.document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    retrieval_service = RetrievalService(
        vector_store_service=VectorStoreService(
            collection_name=document.collection_name
        )
    )

    results = retrieval_service.retrieve(
        document_id=payload.document_id,
        question=payload.question,
        top_k=payload.top_k,
    )

    return {
        "document_id": payload.document_id,
        "question": payload.question,
        "results": results,
    }