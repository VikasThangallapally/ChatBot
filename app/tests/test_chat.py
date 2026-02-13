"""
Tests for chat endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_chat_endpoint(client):
    """Test chat endpoint with valid request."""
    request_data = {"message": "What is a brain tumor?"}
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    assert "explanation" in data
    assert "disclaimer" in data


def test_chat_empty_message(client):
    """Test chat endpoint with empty message."""
    request_data = {"message": ""}
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 422  # Validation error


def test_chat_tumor_query(client):
    """Test chat with tumor-related query."""
    request_data = {"message": "What are the symptoms of a brain tumor?"}
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "tumor" in data["response"].lower() or "abnormal" in data["response"].lower()


def test_chat_mri_query(client):
    """Test chat with MRI-related query."""
    request_data = {"message": "How does MRI detect tumors?"}
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "mri" in data["response"].lower() or "imaging" in data["response"].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
