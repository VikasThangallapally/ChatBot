"""
Tests for prediction endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_predict_no_file(client):
    """Test predict endpoint without file."""
    response = client.post("/api/predict")
    assert response.status_code == 422  # Unprocessable entity


def test_predict_invalid_file(client):
    """Test predict endpoint with invalid file type."""
    data = {"file": ("test.txt", b"not an image", "text/plain")}
    response = client.post("/api/predict", files=data)
    # Should handle invalid file type
    assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
