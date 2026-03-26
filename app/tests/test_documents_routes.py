from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_list_documents_should_return_200() -> None:
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)