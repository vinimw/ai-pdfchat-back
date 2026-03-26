from pathlib import Path

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_upload_should_accept_valid_pdf() -> None:
    file_bytes = (FIXTURES_DIR / "sample.pdf").read_bytes()

    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.pdf", file_bytes, "application/pdf")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "sample.pdf"
    assert body["pages"] >= 1
    assert body["characters"] > 0
    assert isinstance(body["text"], str)


def test_upload_should_reject_non_pdf() -> None:
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.txt", b"text content", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"