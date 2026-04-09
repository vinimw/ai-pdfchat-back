import re

from app.schemas.chunk import DocumentChunk


class ChunkService:
    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 500,
        overlap_words: int = 20,
    ) -> list[DocumentChunk]:
        normalized_text = ChunkService.normalize_text(text)

        if not normalized_text:
            return []

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if overlap_words < 0:
            raise ValueError("overlap_words must be 0 or greater")

        words = normalized_text.split()

        if not words:
            return []

        chunks: list[DocumentChunk] = []
        index = 0
        word_start = 0
        search_start = 0

        while word_start < len(words):
            current_words: list[str] = []
            current_length = 0
            word_end = word_start

            while word_end < len(words):
                word = words[word_end]
                additional_length = len(word) if not current_words else len(word) + 1

                if current_length + additional_length > chunk_size:
                    break

                current_words.append(word)
                current_length += additional_length
                word_end += 1

            if not current_words:
                current_words.append(words[word_start])
                word_end = word_start + 1

            chunk_text = " ".join(current_words)

            start_char = normalized_text.find(chunk_text, search_start)
            if start_char == -1:
                start_char = search_start

            end_char = start_char + len(chunk_text)

            chunks.append(
                DocumentChunk(
                    index=index,
                    text=chunk_text,
                    start_char=start_char,
                    end_char=end_char,
                )
            )

            index += 1
            search_start = start_char

            if word_end >= len(words):
                break

            next_start = max(word_end - overlap_words, word_start + 1)
            word_start = next_start

        return chunks