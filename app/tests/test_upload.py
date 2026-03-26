from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_upload_should_accept_pdf() -> None:
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.pdf", b"fake pdf content", "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.pdf"


def test_upload_should_reject_non_pdf() -> None:
    response = client.post(
        "/api/documents/upload",
        files={"file": ("sample.txt", b"text content", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"