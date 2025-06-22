# Test Configuration
import pytest
import os
import sys
from pathlib import Path

# Add the app directory to Python path
test_dir = Path(__file__).parent
app_dir = test_dir.parent / "app"
sys.path.insert(0, str(app_dir))

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test_taskpilot.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before running tests"""
    # Set test environment variables
    os.environ["DATABASE_URL"] = TEST_DATABASE_URL
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-for-testing"
    os.environ["AI_API_KEY"] = "test-ai-api-key"
    os.environ["DEBUG"] = "true"
    
    yield
    
    # Cleanup after tests
    test_db_path = Path("test_taskpilot.db")
    if test_db_path.exists():
        test_db_path.unlink()

@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test"""
    # This will be called before each test to ensure clean state
    from app.db.session import engine
    from app.models.task_model import Task
    from app.models.user_model import User
    from sqlmodel import SQLModel
    
    # Recreate all tables for each test
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    yield
    
    # Cleanup after each test if needed
    pass

# Pytest configuration
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
