from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_delete_nonexistent_document_should_return_404() -> None:
    response = client.delete("/api/documents/nonexistent-id")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"

def test_download_nonexistent_document_should_return_404() -> None:
    response = client.get("/api/documents/nonexistent-id/file")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"