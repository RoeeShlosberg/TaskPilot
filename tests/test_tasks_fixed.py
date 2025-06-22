import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.main import app

client = TestClient(app)

class TestTaskManagement:
    """Test suite for task CRUD operations"""
    
    @pytest.fixture
    def auth_headers(self):
        """Get authentication headers for testing"""
        # Register and login a test user
        user_data = {
            "username": "taskuser",
            "password": "taskpassword123"
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
    def sample_task_data(self):
        """Sample task data for testing - matches your app's requirements"""
        return {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2025-12-31T23:59:59",
            "priority": "medium",
            "tags": ["test", "development"],
            "mini_tasks": {"subtask1": False, "subtask2": True}
        }
    
    def test_create_task_success(self, auth_headers, sample_task_data):
        """Test successful task creation"""
        response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["priority"] == sample_task_data["priority"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_without_auth(self, sample_task_data):
        """Test task creation without authentication fails"""
        response = client.post("/api/tasks/", json=sample_task_data)
        assert response.status_code == 401
    
    def test_get_all_tasks(self, auth_headers, sample_task_data):
        """Test getting all tasks for authenticated user"""
        # Create a task first
        client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        
        response = client.get("/api/tasks/", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["title"] == sample_task_data["title"]
    
    def test_get_task_by_id(self, auth_headers, sample_task_data):
        """Test getting a specific task by ID"""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == sample_task_data["title"]
    
    def test_get_nonexistent_task(self, auth_headers):
        """Test getting a non-existent task returns 404"""
        response = client.get("/api/tasks/99999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_update_task(self, auth_headers, sample_task_data):
        """Test updating a task"""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Update the task
        update_data = {
            "title": "Updated Task Title",
            "priority": "high"
        }
        response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["priority"] == update_data["priority"]
        # Original description should remain
        assert data["description"] == sample_task_data["description"]
    
    def test_update_task_with_complex_fields(self, auth_headers, sample_task_data):
        """Test updating task with tags and mini_tasks"""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Update with new tags and mini_tasks
        update_data = {
            "tags": ["updated", "new-tag"],
            "mini_tasks": {"new_subtask": False, "completed_subtask": True}
        }
        response = client.put(f"/api/tasks/{task_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert set(data["tags"]) == set(update_data["tags"])
        assert data["mini_tasks"] == update_data["mini_tasks"]
    
    def test_delete_task(self, auth_headers, sample_task_data):
        """Test deleting a task"""
        # Create a task first
        create_response = client.post("/api/tasks/", json=sample_task_data, headers=auth_headers)
        task_id = create_response.json()["id"]
        
        # Delete the task
        response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, auth_headers):
        """Test deleting a non-existent task returns 404"""
        response = client.delete("/api/tasks/99999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_task_validation_missing_title(self, auth_headers):
        """Test task creation with missing title fails"""
        invalid_task = {
            "description": "Task without title",
            "due_date": "2025-12-31T23:59:59"
        }
        response = client.post("/api/tasks/", json=invalid_task, headers=auth_headers)
        assert response.status_code == 400  # Your app returns 400
    
    def test_task_validation_missing_due_date(self, auth_headers):
        """Test task creation with missing due_date fails"""
        invalid_task = {
            "title": "Task without due date",
            "description": "This task has no due date"
        }
        response = client.post("/api/tasks/", json=invalid_task, headers=auth_headers)
        assert response.status_code == 400  # Your app returns 400
    
    def test_task_validation_invalid_priority(self, auth_headers):
        """Test task creation with invalid priority fails"""
        invalid_task = {
            "title": "Test Task",
            "due_date": "2025-12-31T23:59:59",
            "priority": "invalid_priority"
        }
        response = client.post("/api/tasks/", json=invalid_task, headers=auth_headers)
        assert response.status_code == 400  # Your app returns 400
