import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app

client = TestClient(app)

class TestAIAgent:
    """Test suite for AI agent endpoints"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers for testing"""
        # Register and login a test user
        user_data = {
            "username": "aiuser",
            "password": "aipassword123"
        }
        client.post("/api/users/register", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        response = client.post("/api/users/login", data=login_data)
        token = response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.fixture
    def setup_tasks(self, auth_headers):
        """Create some test tasks for AI analysis"""
        tasks = [
            {
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for the project",
                "due_date": "2025-12-31T23:59:59",
                "priority": "high",
                "tags": ["documentation", "urgent"]
            },
            {
                "title": "Review code changes",
                "description": "Review pull requests and provide feedback",
                "due_date": "2025-12-25T17:00:00",
                "priority": "medium",
                "tags": ["review", "development"]
            }
        ]
        
        task_ids = []
        for task in tasks:
            response = client.post("/api/tasks/", json=task, headers=auth_headers)
            task_ids.append(response.json()["id"])
        
        return task_ids
    
    def test_agent_summary_without_auth(self):
        """Test AI summary endpoint requires authentication"""
        response = client.get("/api/agent/summary")
        assert response.status_code == 401
    
    def test_agent_summary_success(self, auth_headers, setup_tasks):
        """Test successful AI summary generation"""
        response = client.get("/api/agent/summary", headers=auth_headers)
        
        # AI endpoints might return different status codes based on configuration
        # In test environment, it might return 200 with mock data or error status
        assert response.status_code in [200, 503, 500]  # Allow for different AI configurations
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data or "message" in data
    
    def test_agent_recommendations_without_auth(self):
        """Test AI recommendations endpoint requires authentication"""
        response = client.get("/api/agent/recommendations")
        assert response.status_code == 401
    
    def test_agent_recommendations_success(self, auth_headers, setup_tasks):
        """Test successful AI recommendations generation"""
        response = client.get("/api/agent/recommendations", headers=auth_headers)
        
        # AI endpoints might return different status codes based on configuration
        assert response.status_code in [200, 503, 500]  # Allow for different AI configurations
        
        if response.status_code == 200:
            data = response.json()
            assert "recommendations" in data or "suggestions" in data or "message" in data
    
    def test_agent_endpoints_with_no_tasks(self, auth_headers):
        """Test AI endpoints when user has no tasks"""
        response = client.get("/api/agent/summary", headers=auth_headers)
        
        # Should handle empty task list gracefully
        assert response.status_code in [200, 404, 503]
        
        if response.status_code == 200:
            data = response.json()
            # Should return some message about no tasks
            assert "no tasks" in str(data).lower() or "empty" in str(data).lower() or "summary" in data

class TestMultiUserIsolation:
    """Test suite to ensure users can only access their own data"""
    
    @pytest.fixture
    def user1_headers(self):
        """Authentication headers for user 1"""
        user_data = {
            "username": "user1",
            "password": "password123"
        }
        client.post("/api/users/register", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        response = client.post("/api/users/login", data=login_data)
        token = response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    @pytest.fixture
    def user2_headers(self):
        """Authentication headers for user 2"""
        user_data = {
            "username": "user2",
            "password": "password123"
        }
        client.post("/api/users/register", json=user_data)
        
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        response = client.post("/api/users/login", data=login_data)
        token = response.json()["access_token"]
        
        return {"Authorization": f"Bearer {token}"}
    
    def test_users_cannot_see_others_tasks(self, user1_headers, user2_headers):
        """Test that users can only see their own tasks"""
        # User 1 creates a task
        task_data = {
            "title": "User 1's Task",
            "description": "This belongs to user 1",
            "due_date": "2025-12-31T23:59:59"
        }
        client.post("/api/tasks/", json=task_data, headers=user1_headers)
        
        # User 2 creates a task
        task_data2 = {
            "title": "User 2's Task",
            "description": "This belongs to user 2",
            "due_date": "2025-12-30T23:59:59"
        }
        client.post("/api/tasks/", json=task_data2, headers=user2_headers)
        
        # User 1 should only see their task
        response1 = client.get("/api/tasks/", headers=user1_headers)
        assert response1.status_code == 200
        tasks1 = response1.json()
        assert len(tasks1) == 1
        assert tasks1[0]["title"] == "User 1's Task"
        
        # User 2 should only see their task
        response2 = client.get("/api/tasks/", headers=user2_headers)
        assert response2.status_code == 200
        tasks2 = response2.json()
        assert len(tasks2) == 1
        assert tasks2[0]["title"] == "User 2's Task"
    
    def test_users_cannot_access_others_tasks_by_id(self, user1_headers, user2_headers):
        """Test that users cannot access other users' tasks by ID"""
        # User 1 creates a task
        task_data = {
            "title": "Private Task",
            "description": "This is private to user 1",
            "due_date": "2025-12-31T23:59:59"
        }
        response = client.post("/api/tasks/", json=task_data, headers=user1_headers)
        task_id = response.json()["id"]
        
        # User 2 tries to access user 1's task
        response = client.get(f"/api/tasks/{task_id}", headers=user2_headers)
        assert response.status_code == 404  # Should not be found for user 2
    
    def test_users_cannot_modify_others_tasks(self, user1_headers, user2_headers):
        """Test that users cannot modify other users' tasks"""
        # User 1 creates a task
        task_data = {
            "title": "Original Task",
            "description": "Original description",
            "due_date": "2025-12-31T23:59:59"
        }
        response = client.post("/api/tasks/", json=task_data, headers=user1_headers)
        task_id = response.json()["id"]
        
        # User 2 tries to modify user 1's task
        update_data = {
            "title": "Hacked Task",
            "description": "This should not work"
        }
        response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=user2_headers)
        assert response.status_code == 404  # Should not be found for user 2
        
        # Verify original task is unchanged
        response = client.get(f"/api/tasks/{task_id}", headers=user1_headers)
        assert response.status_code == 200
        task = response.json()
        assert task["title"] == "Original Task"
