from app.schemas.chunk import DocumentChunk
from app.services.vector_store_service import VectorStoreService


def test_index_and_search_chunks() -> None:
    service = VectorStoreService(collection_name="test_collection")

    chunks = [
        DocumentChunk(index=0, text="Cats are small domestic animals", start_char=0, end_char=30),
        DocumentChunk(index=1, text="Dogs are loyal and friendly animals", start_char=31, end_char=70),
    ]

    embeddings = [
        [0.1, 0.2, 0.3],
        [0.2, 0.1, 0.4],
    ]

    service.index_chunks("doc-1", chunks, embeddings)
    results = service.search(query_embedding=[0.1, 0.2, 0.3], document_id="doc-1", top_k=1)

    assert len(results) == 1
    assert results[0].chunk_index in [0, 1]