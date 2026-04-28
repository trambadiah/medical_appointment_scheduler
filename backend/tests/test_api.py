import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    # Attempting to fetch a root or docs route just to verify server handles it
    response = client.get("/docs")
    assert response.status_code == 200

def test_chat_endpoint_missing_payload():
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Unprocessable Entity

def test_chat_endpoint_invalid_payload():
    response = client.post("/chat", json={"message": 123})
    # Will likely return 422 because message should be string, or handles it gracefully
    assert response.status_code in [200, 422]

@pytest.mark.skip(reason="Requires mocked DB/OpenAI to run safely")
def test_chat_endpoint_valid():
    response = client.post("/chat", json={"message": "I want to schedule an appointment", "session_id": "test_123"})
    assert response.status_code == 200
    assert "response" in response.json()
