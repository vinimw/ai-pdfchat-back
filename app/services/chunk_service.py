from app.schemas.chunk import DocumentChunk


class ChunkService:
    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> list[DocumentChunk]:
        if not text.strip():
            return []

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap < 0:
            raise ValueError("overlap must be 0 or greater")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")

        chunks: list[DocumentChunk] = []
        start = 0
        index = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        index=index,
                        text=chunk_text,
                        start_char=start,
                        end_char=end,
                    )
                )
                index += 1

            if end == text_length:
                break

            start = end - overlap

        return chunks