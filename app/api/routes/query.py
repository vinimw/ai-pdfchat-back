from fastapi import APIRouter

from app.schemas.query import QueryRequest
from app.services.retrieval_service import RetrievalService
from app.services.vector_store_service import VectorStoreService

router = APIRouter(tags=["query"])

@router.post("/documents/query")
async def query_document(payload: QueryRequest):
    vector_store_service = VectorStoreService(
        collection_name=payload.collection_name
    )
    retrieval_service = RetrievalService(
        vector_store_service=vector_store_service
    )

    results = retrieval_service.retrieve(
        document_id=payload.document_id,
        question=payload.question,
        top_k=payload.top_k,
    )

    return {
        "document_id": payload.document_id,
        "collection_name": payload.collection_name,
        "question": payload.question,
        "results": results,
    }