import chromadb


from app.schemas.chunk import DocumentChunk
from app.schemas.retrieval import RetrievedChunk


class VectorStoreService:
    def __init__(self, collection_name: str = "documents") -> None:
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def index_chunks(
        self,
        document_id: str,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        ids = [f"{document_id}:{chunk.index}" for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": chunk.index,
                "start_char": chunk.start_char,
                "end_char": chunk.end_char,
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        document_id: str,
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"document_id": document_id},
        )

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]

        retrieved: list[RetrievedChunk] = []

        for doc, metadata, distance in zip(documents, metadatas, distances):
            retrieved.append(
                RetrievedChunk(
                    chunk_index=int(metadata["chunk_index"]),
                    text=doc,
                    score=float(distance),
                    start_char=int(metadata["start_char"]),
                    end_char=int(metadata["end_char"]),
                )
            )

        return retrieved