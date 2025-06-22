import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app

client = TestClient(app)

class TestUserAuthentication:
    """Test suite for user registration and authentication"""
    
    @pytest.fixture
    def test_user_data(self):
        """Test user data for registration - based on your actual UserCreate schema"""
        return {
            "username": "testuser",
            "password": "testpassword123"
        }
    
    def test_user_registration_success(self, test_user_data):
        """Test successful user registration"""
        response = client.post("/api/users/register", json=test_user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert "id" in data
        assert data["username"] == test_user_data["username"]
        assert "password" not in data  # Password should not be returned
    
    def test_user_registration_duplicate_username(self, test_user_data):
        """Test registration with duplicate username fails"""
        # Register first user
        client.post("/api/users/register", json=test_user_data)
        
        # Try to register with same username
        response = client.post("/api/users/register", json=test_user_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
    
    def test_user_registration_missing_fields(self):
        """Test registration with missing required fields fails"""
        invalid_user = {
            "username": "testuser2"
            # Missing password
        }
        response = client.post("/api/users/register", json=invalid_user)
        assert response.status_code == 400  # Your app returns 400, not 422
    
    def test_user_login_success(self, test_user_data):
        """Test successful user login"""
        # Register user first
        client.post("/api/users/register", json=test_user_data)
        
        # Login with form data (OAuth2PasswordRequestForm expects form data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/users/login", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials fails"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        response = client.post("/api/users/login", data=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_protected_endpoint_without_token(self):
        """Test that protected endpoints require authentication"""
        response = client.get("/api/tasks/")
        assert response.status_code == 401
    
    def test_protected_endpoint_with_invalid_token(self):
        """Test that protected endpoints reject invalid tokens"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/tasks/", headers=headers)
        assert response.status_code == 401
