from fastapi import APIRouter

from app.schemas.chat import ChatAskRequest
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])


@router.post("/chat/ask")
async def ask_question(payload: ChatAskRequest):
    chat_service = ChatService()

    response = chat_service.ask(
        document_id=payload.document_id,
        collection_name=payload.collection_name,
        question=payload.question,
        top_k=payload.top_k,
    )

    return response