from app.schemas.retrieval import RetrievedChunk
from app.services.chat_service import ChatService


class FakeLlmService:
    def generate(self, prompt: str) -> str:
        return "This document is about software testing."


class FakeRetrievalService:
    def retrieve(self, document_id: str, question: str, top_k: int = 3):
        return [
            RetrievedChunk(
                chunk_index=0,
                text="This PDF is about software testing.",
                score=0.1,
                start_char=0,
                end_char=35,
            )
        ]


def test_chat_service_should_return_answer_and_sources() -> None:
    service = ChatService(
        llm_service=FakeLlmService(),
        retrieval_service=FakeRetrievalService(),
    )

    response = service.ask(
        document_id="doc-1",
        collection_name="collection-1",
        question="What is this PDF about?",
        top_k=3,
    )

    assert response.answer == "This document is about software testing."
    assert len(response.sources) == 1
    assert response.sources[0].chunk_index == 0