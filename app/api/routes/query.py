from fastapi import APIRouter

from app.schemas.query import QueryRequest
from app.services.retrieval_service import RetrievalService

router = APIRouter(tags=["query"])

@router.post("/documents/query")
async def query_document(payload: QueryRequest):
    retrieval_service = RetrievalService()
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