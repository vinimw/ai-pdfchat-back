import pytest

from app.services.chunk_service import ChunkService


def test_split_text_should_return_empty_list_for_blank_text() -> None:
    chunks = ChunkService.split_text("   ")

    assert chunks == []


def test_split_text_should_create_chunks() -> None:
    text = "A" * 1200

    chunks = ChunkService.split_text(text, chunk_size=500, overlap=100)

    assert len(chunks) == 3
    assert chunks[0].index == 0
    assert chunks[1].index == 1
    assert chunks[2].index == 2
    assert len(chunks[0].text) > 0


def test_split_text_should_apply_overlap() -> None:
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = ChunkService.split_text(text, chunk_size=10, overlap=2)

    assert chunks[0].text == "ABCDEFGHIJ"
    assert chunks[1].text == "IJKLMNOPQR"
    assert chunks[2].text == "QRSTUVWXYZ"


def test_split_text_should_raise_for_invalid_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        ChunkService.split_text("example text", chunk_size=0)


def test_split_text_should_raise_for_negative_overlap() -> None:
    with pytest.raises(ValueError, match="overlap must be 0 or greater"):
        ChunkService.split_text("example text", overlap=-1)


def test_split_text_should_raise_when_overlap_is_too_large() -> None:
    with pytest.raises(ValueError, match="overlap must be smaller than chunk_size"):
        ChunkService.split_text("example text", chunk_size=100, overlap=100)