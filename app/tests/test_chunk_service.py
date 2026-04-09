import pytest

from app.services.chunk_service import ChunkService


def test_split_text_should_return_empty_list_for_blank_text() -> None:
    chunks = ChunkService.split_text("   ")
    assert chunks == []


def test_split_text_should_not_break_words() -> None:
    text = "This is a simple sentence for chunk testing and readability."

    chunks = ChunkService.split_text(text, chunk_size=20, overlap_words=2)

    assert len(chunks) > 0

    for chunk in chunks:
        assert "  " not in chunk.text
        assert chunk.text == chunk.text.strip()


def test_split_text_should_create_readable_chunks() -> None:
    text = (
        "FastAPI is a modern web framework for building APIs with Python. "
        "It is fast, simple, and developer friendly."
    )

    chunks = ChunkService.split_text(text, chunk_size=50, overlap_words=3)

    assert len(chunks) >= 2
    assert all(len(chunk.text) > 0 for chunk in chunks)


def test_split_text_should_apply_word_overlap() -> None:
    text = "one two three four five six seven eight nine ten"

    chunks = ChunkService.split_text(text, chunk_size=18, overlap_words=2)

    assert len(chunks) >= 2
    assert "three" in chunks[1].text or "four" in chunks[1].text


def test_split_text_should_raise_for_invalid_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        ChunkService.split_text("example text", chunk_size=0)


def test_split_text_should_raise_for_negative_overlap_words() -> None:
    with pytest.raises(ValueError, match="overlap_words must be 0 or greater"):
        ChunkService.split_text("example text", overlap_words=-1)