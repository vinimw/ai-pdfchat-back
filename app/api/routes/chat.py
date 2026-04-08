from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import ChatAskRequest
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])


@router.post("/chat/ask")
async def ask_question(
    payload: ChatAskRequest,
    db: Session = Depends(get_db),
):
    try:
        chat_service = ChatService(db=db)
        return chat_service.ask(
            document_id=payload.document_id,
            question=payload.question,
            top_k=payload.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc