from app.services.embedding_service import EmbeddingService

def test_embed_texts_should_return_embeddings() -> None:
    service = EmbeddingService()
    embeddings = service.embed_texts(["hello world", "another sentence"])

    assert len(embeddings) == 2
    assert len(embeddings[0]) > 0