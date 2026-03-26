from io import BytesIO

from pypdf import PdfReader

from app.core.exceptions import EmptyPdfError, InvalidPdfError

class PdfService:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes) -> tuple[str, int]:
        if not file_bytes:
            raise InvalidPdfError("PDF file is empty or invalid")

        try:
            reader = PdfReader(BytesIO(file_bytes))
        except Exception as exc:
            raise InvalidPdfError("Could not read PDF file") from exc

        texts: list[str] = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            cleaned = page_text.strip()
            if cleaned:
                texts.append(cleaned)

        full_text = "\n\n".join(texts).strip()
        total_pages = len(reader.pages)

        if not full_text:
            raise EmptyPdfError("PDF does not contain readable text")

        return full_text, total_pages