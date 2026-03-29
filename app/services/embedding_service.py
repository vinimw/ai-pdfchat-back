from hashlib import sha256

from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            self.model = None

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        if self.model is None:
            return [self._fallback_embedding(text) for text in texts]

        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        if self.model is None:
            return self._fallback_embedding(text)

        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    @staticmethod
    def _fallback_embedding(text: str) -> list[float]:
        digest = sha256(text.encode("utf-8")).digest()
        return [byte / 255 for byte in digest]
