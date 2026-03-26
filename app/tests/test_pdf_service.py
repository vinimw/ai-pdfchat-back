from pathlib import Path

import pytest

from app.core.exceptions import EmptyPdfError, InvalidPdfError
from app.services.pdf_service import PdfService


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_extract_text_from_valid_pdf() -> None:
    file_bytes = (FIXTURES_DIR / "sample.pdf").read_bytes()

    text, pages = PdfService.extract_text_from_bytes(file_bytes)

    assert pages >= 1
    assert isinstance(text, str)
    assert len(text) > 0


def test_extract_text_should_raise_for_empty_bytes() -> None:
    with pytest.raises(InvalidPdfError, match="PDF file is empty or invalid"):
        PdfService.extract_text_from_bytes(b"")


def test_extract_text_should_raise_for_invalid_pdf() -> None:
    with pytest.raises(InvalidPdfError):
        PdfService.extract_text_from_bytes(b"not a real pdf")