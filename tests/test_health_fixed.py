import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Test suite for health check endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        assert "welcome" in response.json()["message"].lower()
    
    def test_health_endpoint(self):
        """Test the health check endpoint returns 200 OK"""
        response = client.get("/health")
        assert response.status_code == 200
        
        # Check response structure based on your actual response
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        
        # Check for actual fields returned by your app
        expected_fields = ["status", "app", "version"]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"

class TestAPIDocumentation:
    """Test that API documentation endpoints are accessible"""
    
    def test_openapi_json_accessible(self):
        """Test that OpenAPI JSON schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    def test_docs_page_accessible(self):
        """Test that Swagger UI docs page is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
